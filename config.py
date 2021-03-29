class DevConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql:///kids_krafts"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SECRET_KEY = "shhhhh it's a secret"

class TestConfig(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql:///kids_krafts_test'
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO = False
    TESTING = True
    SECRET_KEY = "shhhhh it's a secret"

class ProdConfig(object):
    DEBUG = False
    DATABASE_URL = ""


app_config = {
    'DEFAULT': DevConfig,
    'TESTING': TestConfig,
    'DEVELOPMENT': DevConfig,
    'PRODUCTION': ProdConfig,
}