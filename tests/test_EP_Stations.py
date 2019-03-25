from app import app
from tests.fixtures import *


def test_get_stations_list(clean_test_data, test_db_config):
    """
    Получаем список заправок
    :return:
    """
    ret_raw = app.test_client().get(
        "/api/v1/fuel/stations")

    assert ret_raw.status_code == 200
    ret = ret_raw.json

    assert ret["success"] is True
