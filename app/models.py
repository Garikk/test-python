from sqlalchemy.orm import relationship

from app import db


class GasStations(db.Model):
    __tablename__ = "gas_stations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    is_open = db.Column(db.Boolean)

    def __repr__(self):
        return "<id {}>".format(self.id)


class FuelTypes(db.Model):
    __tablename__ = "fuel_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return "<id {}>".format(self.id)


class GasStationFuel(db.Model):
    __tablename__ = "gas_stations_fuel"

    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey("gas_stations.id", onupdate="CASCADE", ondelete="CASCADE"))
    fuel_id = db.Column(db.Integer, db.ForeignKey("fuel_types.id", onupdate="CASCADE", ondelete="CASCADE"))
    cost = db.Column(db.Float)

    station = relationship("GasStations", backref="avail_fuels")
    fuel = relationship("FuelTypes", backref="avail_on_stations")

    def __repr__(self):
        return "<id {}>".format(self.id)


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return "<id {}>".format(self.id)


class CarType(db.Model):
    __tablename__ = "car_type"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    fuel_type = db.Column(db.Integer, db.ForeignKey("fuel_types.id", onupdate="CASCADE", ondelete="CASCADE"))
    liter_per_km = db.Column(db.Integer)

    def __repr__(self):
        return "<id {}>".format(self.id)


class CarUser(db.Model):
    __tablename__ = "car_user"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"))
    car_id = db.Column(db.Integer, db.ForeignKey("car_type.id", onupdate="CASCADE", ondelete="CASCADE"))
    active = db.Column(db.Boolean, default=False)

    user = relationship("User", backref="cars")
    car = relationship("CarType", backref="car_users")
