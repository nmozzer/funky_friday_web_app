from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    STATIC_FOLDER = 'static'
    SECRET_KEY = environ.get('SECRET_KEY')
    TEMPLATES_FOLDER = 'templates'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    FLASK_ENV = 'prod'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URI')


class DevConfig(Config):
    FLASK_ENV = 'dev'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URI')

class TestConfig(Config):
    FLASK_ENV = 'test'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    LOGIN_DISABLED = True