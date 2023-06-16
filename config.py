import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False

    SESSION_COOKIE_SAMESITE = 'None'

    # Swagger Configuration
    RESTX_MASK_SWAGGER = False
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_ACCESS_TOKEN_EXPIRES = 1500
    UPLOAD_FOLDER = os.path.join(basedir, 'app/main/static/upload/')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    # MTA Configuration
    MAIL_SERVER = 'mail.xxx.com'
    MAIL_PORT = 123
    MAIL_USERNAME = 'xxx@xxx.com'
    MAIL_PASSWORD = 'passpasspass'
    MAIL_USE_TLS = True



class DevelopmentConfig(BaseConfig):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    # HOST = "172.16.0.193"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app/main/phishing.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = 3600*24


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app/main/phishing.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(BaseConfig):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = BaseConfig.SECRET_KEY
