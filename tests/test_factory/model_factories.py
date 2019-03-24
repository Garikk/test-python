from factory import Factory
from datetime import datetime

from app.models import FuelTypes, GasStations, GasStationFuel, User, CarType, CarUser


class FuelTypesFactory(Factory):
    class Meta:
        model = FuelTypes

    name = "TestFuel"


class GasStationFactory(Factory):
    class Meta:
        model = GasStations

    name = "Test Station"
    is_open = True


class GasStationFuelFactory(Factory):
    class Meta:
        model = GasStationFuel()

    station_id = None
    fuel_id = None
    cost = None


class UserFactory(Factory):
    class Meta:
        model = User

    name = "Test User"


class CarTypeFactory(Factory):
    class Meta:
        model = CarType

    name = "Test Car"
    liter_per_km = 10


class CarUserFactory(Factory):
    class Meta:
        model = CarUser

    user_id = None
    car_id = None
    active = True
