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
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'kidskrafts4u@gmail.com'
    MAIL_PASSWORD = environ.get('email_password')
    STRIPE_SECRET_KEY = environ.get('stripe_secret_key')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = 'static/images'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

class TestConfig(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@postgres:5432/kids_krafts_test'
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO = False
    TESTING = True
    SECRET_KEY = environ.get('secret_key')
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'kidskrafts4u@gmail.com'
    MAIL_PASSWORD = environ.get('email_password')
    STRIPE_SECRET_KEY = environ.get('stripe_secret_key')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = 'static/images'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

class ProdConfig(object):
    ENV = 'production'
    WTF_CSRF_ENABLED = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
    SECRET_KEY = environ.get('secret_key')
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'kidskrafts4u@gmail.com'
    MAIL_PASSWORD = environ.get('email_password')
    STRIPE_SECRET_KEY = environ.get('stripe_secret_key')
    SESSION_TYPE = 'filesystem'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = 'static/images'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app_config = {
    'DEFAULT': DevConfig,
    'TESTING': TestConfig,
    'DEVELOPMENT': DevConfig,
    'PRODUCTION': ProdConfig,
}