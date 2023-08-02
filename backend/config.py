import os.path
from dotenv import load_dotenv

# в прошлом проекте у меня также не работало, так как внешний .env не копировался в контейнер, так что
# нужно в любом случае два .env файла, один для Dockerfile2, другой для compose

# basedir = os.path.abspath(os.path.dirname(__file__))
# # basedir = '/'.join(basedir.split('/')[:-1])
# print('*****************************************')
# print(basedir)
# print('*****************************************')
# basedir = basedir+'/backend/'
# print(basedir)
# load_dotenv(os.path.join(basedir, '.env'))

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    REMEMBER_COOKIE_HTTPONLY = False
    ADMINS = os.environ.get('ADMINS')
    MAIN_ADMIN_EMAIL = os.environ.get('MAIN_ADMIN_EMAIL')
    basepath = os.path.abspath("") + '/'


class DevelopmentConfig(Config):
    name = 'DevelopmentConfig'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_POSTGRES_dev')
    # REDIS_URL = os.environ.get('REDIS_URL_LOCAL')


class TestingConfig(Config):
    name = 'TestingConfig'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_POSTGRES_test')
    # REDIS_URL = os.environ.get('REDIS_URL_LOCAL')


class ProductionConfig(Config):
    name = 'ProductionConfig'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_POSTGRES_prod')
    # REDIS_URL = os.environ.get('REDIS_URL_server')
