import os.path
from dotenv import load_dotenv, find_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
basedir = '/'.join(basedir.split('/')[:-1])

load_dotenv(os.path.join(basedir, '.env'))
# load_dotenv(find_dotenv())


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = os.environ.get('ADMINS')
    ADMIN_LOGIN = os.environ.get('ADMIN_LOGIN')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
    basepath = os.path.abspath("") + '/'





class DevelopmentConfig(Config):
    name = 'DevelopmentConfig'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_POSTGRES_dev')
    REDIS_URL = os.environ.get('REDIS_URL_LOCAL')


class TestingConfig(Config):
    name = 'TestingConfig'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_POSTGRES_test')
    # REDIS_URL = os.environ.get('REDIS_URL_LOCAL')


class ProductionConfig(Config):
    name = 'ProductionConfig'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_POSTGRES_prod')
    # REDIS_URL = os.environ.get('REDIS_URL_server')