import pytest

from app import db
from app.models import CarUser, CarType, GasStations, FuelTypes, User, GasStationFuel
from tests.test_factory.model_factories import FuelTypesFactory, GasStationFactory, CarUserFactory, UserFactory, \
    CarTypeFactory, GasStationFuelFactory


def create_fuel_type(name="TestFuel"):
    new_ft = FuelTypesFactory()
    new_ft.name = name
    db.session.add(new_ft)
    db.session.commit()
    return new_ft.id


def create_station(name="test_station", is_open=True):
    new_st = GasStationFactory()
    new_st.is_open = is_open
    new_st.name = name
    db.session.add(new_st)
    db.session.commit()
    return new_st.id


def create_user(id, name="test_user"):
    new_us = UserFactory()
    new_us.id = id
    new_us.name = name
    db.session.add(new_us)
    db.session.commit()
    return new_us.id


def create_car(id, name="test_user", liter_per_100km=10):
    new_cr = CarTypeFactory()
    new_cr.id = id
    new_cr.name = name
    new_cr.liter_per_km = liter_per_100km
    db.session.add(new_cr)
    db.session.commit()
    return new_cr.id


def create_usercar(user, car, active):
    new_uc = CarUserFactory()
    new_uc.car_id = car
    new_uc.user_id = user
    new_uc.active = active
    db.session.add(new_uc)
    db.session.commit()
    return new_uc.id


def assign_station_fuel(fuel_id, station_id, cost):
    new_fa = GasStationFuelFactory()
    new_fa.fuel_id = fuel_id
    new_fa.station_id = station_id
    new_fa.cost = cost
    db.session.add(new_fa)
    db.session.commit()


@pytest.fixture()
def test_db_config():
    user = create_user(1, "User1")
    user2 = create_user(2, "User2")
    user3 = create_user(3, "User3")

    station_1_open = create_station("ST_1", True)
    station_2_open = create_station("ST_2", True)
    station_3_close = create_station("ST_3", False)
    station_4_open = create_station("ST_4", True)

    assign_station_fuel(fuel_id=1, station_id=station_1_open, cost=40)
    assign_station_fuel(fuel_id=2, station_id=station_1_open, cost=44)
    assign_station_fuel(fuel_id=3, station_id=station_1_open, cost=42)

    assign_station_fuel(fuel_id=1, station_id=station_2_open, cost=39)
    assign_station_fuel(fuel_id=2, station_id=station_2_open, cost=43)
    assign_station_fuel(fuel_id=4, station_id=station_2_open, cost=41.50)

    assign_station_fuel(fuel_id=1, station_id=station_3_close, cost=44)
    assign_station_fuel(fuel_id=3, station_id=station_3_close, cost=48)
    assign_station_fuel(fuel_id=4, station_id=station_3_close, cost=46)

    assign_station_fuel(fuel_id=2, station_id=station_4_open, cost=46)
    assign_station_fuel(fuel_id=3, station_id=station_4_open, cost=50)
    assign_station_fuel(fuel_id=4, station_id=station_4_open, cost=51)

    create_usercar(user, 1, active=False)
    create_usercar(user, 2, active=False)
    create_usercar(user, 3, active=True)
    create_usercar(user2, 3, active=True)
    create_usercar(user3, 1, active=True)


@pytest.fixture()
@pytest.mark.order(0)
def clean_test_data():
    """
    Очищает БД от тестовых данных текущей сессии тестирования
    :return:
    """
    User.query.delete()
    CarUser.query.delete()
    GasStations.query.delete()
    GasStationFuel.query.delete()
