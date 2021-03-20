class DevConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql:///kids_krafts"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

class TestConfig(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql:///kids_krafts_test'
    SQLALCHEMY_ECHO = False
    TESTING = True

class ProdConfig(object):
    DEBUG = False
    DATABASE_URL = ""


app_config = {
    'DEFAULT': DevConfig,
    'TESTING': TestConfig,
    'DEVELOPMENT': DevConfig,
    'PRODUCTION': ProdConfig,
}