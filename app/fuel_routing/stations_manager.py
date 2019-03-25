from collections import namedtuple

from app import db
from app.exceptions import SvsException
from app.external.stations import StationsService
from app.models import CarType, GasStations, GasStationFuel, CarUser


class StationsManager():
    def stations(self, args):
        """
        Возвращаем список станций с топливом до которых мы можем доехат по условиям
        :param args: Параметры
        :return: массив с id станции
        """
        car_id = self._get_arg_attr(args=args, arg='car_id')
        user_id = self._get_arg_attr(args=args, arg='user_id')
        required_fuel = self._get_arg_attr(args=args, arg='required_fuel')
        time_limit = self._get_arg_attr(args=args, arg='time_limit')
        car_fuel_level = self._get_arg_attr(args=args, arg='car_fuel_level')
        avg_speed = self._get_arg_attr(args=args, arg='avg_speed')
        avail_money = self._get_arg_attr(args=args, arg='avail_money')

        if avg_speed is None:
            avg_speed = 30

        # Это у нас обязательные параметры, без них мы ничего не посчитаем, остальное проверяется в маршмеллоу сериалайзере
        if car_id is None and user_id is None:
            raise SvsException(result_code=400, message="car_id or user_id is required")

        # Получаем активный автомобиль пользователя, если он не указан напрямую
        if car_id is None:
            car_id = self._get_user_car(user_id=user_id)
            car = CarType.query.get(car_id)
        else:
            car = CarType.query.get(car_id)

        # Получаем список расстояний до заправок из внешнего сервиса
        stations_list = StationsService().get_stations_for_point(coords="my_current_geo_coords_here")

        # Получаем максимальное расстояние до которого мы можем доехать до заправки
        if time_limit is not None:
            time_limit_to_station = time_limit / 2  # половинное время, потому что надо ещё вернуться
        else:
            time_limit_to_station = None

        car_distance = self._get_max_distance(car_id=car_id, avg_speed=avg_speed, avail_fuel_level=car_fuel_level,
                                              time_limit=time_limit_to_station)
        # проверяем доступность станций и совпадение условий

        req = db.session.query(GasStations.id, GasStationFuel.cost).join(GasStationFuel,
                                                                         GasStations.id == GasStationFuel.station_id).filter(
            GasStationFuel.fuel_id == car.fuel_type,
            GasStationFuel.cost.isnot(None),
            GasStations.id.in_(stations_list.keys())).filter(GasStations.is_open.is_(True))

        ret = []
        for item in req:
            # Проверяем что заправка в зоне доступности
            if stations_list[item[0]] <= car_distance:
                if avail_money is not None:
                    # проверяем хватит ли нам денег на этой заправке
                    # по хорошему это надо вынести сразу в запрос, но сделаем пока так
                    if (item['cost'] * required_fuel) >= avail_money:
                        continue
                # Проверяем что нам хватит топлива чтобы вернуться
                remaining_fuel = self._get_fuel_remaining(car_id=car_id, from_fuel_level=car_fuel_level,
                                                          distance=stations_list[item[0]])
                remaining_fuel = remaining_fuel + required_fuel  # учитываем заправленный бензин
                return_distance = self._get_max_distance(car_id=car_id, avg_speed=avg_speed,
                                                         avail_fuel_level=remaining_fuel)
                # Если нам не хватит топлива чтобы вернуться, пропускаем
                # Время на возврат уже заложено в пером расчете доступности заправок, по этому можно его не учитывать
                if return_distance < stations_list[item[0]]:
                    continue

                ret.append({
                    "id": item.id,
                    "distance_to_station": stations_list[item[0]],
                    "cost": item.cost
                })

        return ret

    def _get_user_car(self, user_id):
        """
        Возвращает активный автомобиль пользователя
        :param user_id: идентификатор пользователя
        :return:
        """
        return db.session.query(CarUser.car_id).filter(CarUser.user_id == user_id,
                                                       CarUser.active.is_(True)).one_or_none()

    def _get_fuel_remaining(self, car_id, from_fuel_level, distance):
        """
        Расчет остатка топлива после преодоления определенного расстояния
        :param car_id: идентификатор автомобиля
        :param from_fuel_level: исходный объем топлива
        :param distance: расстояние которое надо приодолеть
        :return:
        """
        car = CarType.query.get(car_id)
        fuel = (car.liter_per_km / 100) * distance
        return from_fuel_level - fuel

    def _get_max_distance(self, car_id, avg_speed=30, avail_fuel_level=None, time_limit=None):
        """
        Возвращаем максимальное расстояние которое может преодолеть авто с указанными параметрами
        :param car_id:
        :param avg_speed:
        :param avail_fuel_level:
        :param time_limit:
        :return:
        """
        car = CarType.query.get(car_id)

        fuel_distance = (100 / car.liter_per_km) * avail_fuel_level
        if time_limit is None:
            time_distance = 0
        else:
            time_distance = avg_speed * (time_limit * 60 * 60)

        max_distance = max((time_distance, fuel_distance))

        return max_distance

    def _get_arg_attr(self, arg, args):
        """
        Процедура для парсига входных параметров из marshmellow
        :param arg:
        :param args:
        :return:
        """
        if arg in args and args[arg] is not None:
            return args[arg]

        return None
