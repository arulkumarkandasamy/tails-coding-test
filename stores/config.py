import os
import logging


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = '1d94e52c-1c89-4515-b87a-f48cf3cb7f0b'
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'stores.log'
    LOGGING_LEVEL = logging.DEBUG
    SECURITY_PASSWORD_SALT = '8312hjf123'
    CACHE_TYPE = 'simple'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    ENV = 'dev'
    SECRET_KEY = 'a9eec0e0-23b7-4788-9a92-318347b9a39f'


class StagingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    ENV = 'staging'
    SECRET_KEY = '792842bc-c4df-4de1-9177-d5207bd9faa6'


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    ENV = 'prod'
    SECRET_KEY = '8c0caeb1-6bb2-4d2d-b057-596b2dcab18e'


config = {
    "dev": "stores.config.DevelopmentConfig",
    "staging": "stores.config.StagingConfig",
    "prod": "stores.config.ProductionConfig",
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
