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
        required_fuel_type = self._get_arg_attr(args=args, arg='required_fuel_type')
        time_limit = self._get_arg_attr(args=args, arg='time_limit')
        car_fuel_level = self._get_arg_attr(args=args, arg='car_fuel_level')
        avg_speed = self._get_arg_attr(args=args, arg='avg_speed')
        avail_money = self._get_arg_attr(args=args, arg='avail_money')

        # Это у нас обязательные параметры, без них мы ничего не посчитаем, остальное проверяется в маршмеллоу сериалайзере
        if car_id is None and user_id is None:
            raise SvsException(result_code=400, message="car_id or user_id is required")

        # Получаем активный автомобиль пользователя, если он не указан напрямую
        if car_id is None:
            car_id = self._get_user_car(user_id=user_id)

        # Получаем список расстояний до заправок из внешнего сервиса
        stations_list = StationsService().get_stations_for_point(coords="my_current_geo_coords_here")

        # Получаем максимальное расстояние до которого мы можем доехать
        car_distance = self._get_max_distance(car_id=car_id, avg_speed=avg_speed, avail_fuel_level=car_fuel_level,
                                              time_limit=time_limit)

        # проверяем доступность станций и совпадение условий

        req = db.session.query(GasStations, GasStationFuel.cost).join(GasStationFuel,
                                                                      GasStations.id == GasStationFuel.fuel_id).filter(
            GasStations.is_open.is_(True), GasStationFuel.fuel_id == required_fuel_type,
            GasStationFuel.cost.isnot(None),
            GasStations.id.in_(stations_list.keys()))

        ret = []
        for item in req:
            # Проверяем что заправка в зоне доступности
            # Удваиваем расстояние для учета того что возвращаемся
            if item['distance'] * 2 <= car_distance:
                if avail_money is not None:
                    # проверяем хватит ли нам денег на этой заправке
                    # по хорошему это надо вынести сразу в запрос, но сделаем пока так
                    if (item['cost'] * required_fuel) >= avail_money:
                        continue

                ret.append({
                    "id": item.id,
                    "distance": car_distance[item.id]['distance'],
                    "cost": item.cost
                })

        return ret

    def _get_user_car(self, user_id):
        return db.session.query(CarUser.car_id).filter(CarUser.user_id == user_id,
                                                       CarUser.active.is_(True)).one_or_none()

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

        fuel_distance = (car.liter_per_100km / 100) * avail_fuel_level
        time_distance = avg_speed * (time_limit * 60 * 60)

        max_distance = max((time_distance, fuel_distance))

        return max_distance

    def _get_arg_attr(self, arg, args):
        if arg in args and args[arg] is not None:
            return args[arg]

        return None
