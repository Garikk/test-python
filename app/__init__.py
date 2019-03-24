import os

from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

if os.environ.get('FLASK_ENV', "production") == "development":
    app.config.from_object('config.DevelopmentConfig')
    print("[WARN] !! Using development config !!")
elif os.environ.get('FLASK_ENV', "production") == "test":
    app.config.from_object('config.TestingConfig')
    print("[WARN] !! Using test config !! Use this mode ONLY for pytest !!")
else:
    app.config.from_object('config.ProductionConfig')

db = SQLAlchemy(app)

from app import models  # noqa: E402  -- Исключение для Flake8

manager = Manager(app)
manager.add_command('db', MigrateCommand)

migrate = Migrate(app, models.db)
manager = Manager(app)

from app.router import Router  # noqa: E402

api = Api(app)

Router(api)
