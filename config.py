import os

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "9asdf6b8a7b6sde89f6b7e7f6asd6fb"

    UPLOAD_FOLDER = 'uploads'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    FILE_PATH = os.path.join(BASEDIR, UPLOAD_FOLDER, "food_image")
    # SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost:3306/sirkadian"
    SQLALCHEMY_DATABASE_URI = "mysql://freedbtech_sirkadian:pokoknyabakalsukses@freedb.tech:3306/freedbtech_sirkadian"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'sirkadiancorporation@gmail.com'
    MAIL_PASSWORD = 'pokoknyabakalsukses'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    FLASK_ADMIN_SWATCH = 'cerulean'

    SESSION_COOKIE_SECURE = True

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    # DEBUG = True
    
    # SESSION_COOKIE_SECURE = False
    pass

class TestingConfig(Config):
    TESTING = True

    SESSION_COOKIE_SECURE = False
