from os.path import join, dirname, realpath

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "9asdf6b8a7b6sde89f6b7e7f6asd6fb"

    UPLOAD_FOLDER = 'uploads'
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost:3306/sirkadian"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    SESSION_COOKIE_SECURE = True

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

    SESSION_COOKIE_SECURE = False
