import os


class Config(object):
    """
    Объект конфигурации приложения, базовый
    """
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # SQLAlchemy config
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 200
    SQLALCHEMY_POOL_TIMEOUT = 20


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
