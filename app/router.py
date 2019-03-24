from app.fuel_routing.resources import FuelRouting


class Router:
    def __init__(self, api):
        api.add_resource(FuelRouting, "/api/v1/fuel/stations", methods=['GET'])
