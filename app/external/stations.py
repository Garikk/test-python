import random

from app import db
from app.models import GasStations


class StationsService():
    def get_stations_for_point(self, coords):
        """
        Возвращает список заправок в в указанном диапазоне расстояний
        :return:
        """

        # Тут по условиям должен быть вызов во внешний сервис, но т.к. нет, то хардкодим ответ
        # Возвращаем список имеющихся у нас станций с рандомными расстояниями
        data = []
        req = db.session.query(GasStations.id)
        for item in req:
            data.append({"id": item.id, "distance": random.randint(1, 500)})
        #
        # Делаем удобный доступ для использования
        ret = {}
        for item in data:
            ret[item['id']] = item['distance']

        return ret
