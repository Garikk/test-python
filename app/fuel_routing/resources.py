from flask import request
from flask_restful import Resource

from app.api_wrappers import api_response, svs_exceptions, svsApiResponse
from app.fuel_routing.serializers import stations_locator_schema
from app.fuel_routing.stations_manager import StationsManager


class FuelRouting(Resource):
    @api_response
    @svs_exceptions
    def get(self):
        """
        @api { get } /api/v1/fuel_station Возвращает заправки по вводным данным
        @apiGroup Fuel stations
        @apiVersion 1.0.0
        """
        manager = StationsManager()
        # Раньше, по феншую тут надо было использовать Argparser, но он уже deprecated по этому юзаем marshmellow
        args = stations_locator_schema.load(request.args)

        data = manager.stations(args=args.data)
        return svsApiResponse(data=data)
