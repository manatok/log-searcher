import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'jwt_secret_signing_key')
    ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL', 'elasticsearch:9200')
    REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
    REDIS_PORT = os.getenv('REDIS_PORT', 6379)
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', 'password')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
