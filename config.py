from os import path, environ
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class DevConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql:///kids_krafts"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SECRET_KEY = environ.get('secret_key')

class TestConfig(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql:///kids_krafts_test'
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO = False
    TESTING = True
    SECRET_KEY = environ.get('secret_key')

class ProdConfig(object):
    DEBUG = False
    DATABASE_URL = ""


app_config = {
    'DEFAULT': DevConfig,
    'TESTING': TestConfig,
    'DEVELOPMENT': DevConfig,
    'PRODUCTION': ProdConfig,
}