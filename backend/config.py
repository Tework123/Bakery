import os.path
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    # application settings
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # sentry settings
    dsn = os.environ.get('dsn')

    # flask-login settings for user backend cookies on frontend
    REMEMBER_COOKIE_HTTPONLY = False

    # mail settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # admins settings
    ADMINS = os.environ.get('ADMINS')
    MAIN_ADMIN_EMAIL = os.environ.get('MAIN_ADMIN_EMAIL')

    basepath = os.path.abspath("") + '/'


class DevelopmentConfig(Config):
    name = 'DevelopmentConfig'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_POSTGRES_dev')
    SENTRY_ENV = 'development'


class TestingConfig(Config):
    name = 'TestingConfig'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_POSTGRES_test')


class ProductionConfig(Config):
    name = 'ProductionConfig'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_POSTGRES_prod')
    SENTRY_ENV = 'production'
