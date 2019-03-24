from marshmallow import Schema, fields

from app.validators import validate_blank


class StationsLocatorGet(Schema):
    user_id = fields.Integer(
        required=False, validate=validate_blank('USER_ID'),
        error_messages={'null': 'USER_ID_BLANK', 'required': 'USER_ID_DATE'}
    )
    car_id = fields.Integer(
        required=False, validate=validate_blank('CAR_ID'),
        error_messages={'null': 'CAR_ID_BLANK', 'required': 'CAR_ID'}
    )
    car_fuel_level = fields.Integer(
        required=True, validate=validate_blank('CAR_FUEL_LEVEL'),
        error_messages={'null': 'CAR_FUEL_LEVEL_BLANK', 'required': 'CAR_FUEL_LEVEL'}
    )
    required_fuel = fields.Integer(reqired=True, validate=validate_blank('FUEL_REQUIRED'),
                                   error_messages={'null': 'FUEL_REQUIRED_BLANK', 'required': 'FUEL_REQUIRED'}
                                   )
    required_fuel_amount = fields.Integer(reqired=True, validate=validate_blank('FUEL_REQUIRED_AMOUNT'),
                                          error_messages={'null': 'FUEL_REQUIRED_AMOUNT_BLANK',
                                                          'required': 'FUEL_REQUIRED_AMOUNT'}
                                          )
    time_limit = fields.Float(
        required=False, validate=validate_blank('TIME_LIMIT'),
        error_messages={'null': 'TIME_LIMIT_BLANK', 'required': 'TIME_LIMIT'}
    )


stations_locator_schema = StationsLocatorGet()
