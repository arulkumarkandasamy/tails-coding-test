import os
import logging


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'stores.log'
    LOGGING_LEVEL = logging.DEBUG
    CACHE_TYPE = 'simple'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    ENV = 'dev'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tails_store.db'


config = {
    "dev": "stores.config.DevelopmentConfig",
    "default": "stores.config.DevelopmentConfig"
}


def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.cfg', silent=True)
    # Configure logging
    handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
