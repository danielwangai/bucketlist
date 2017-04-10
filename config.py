import os

class Config(object):
    """
    Common configuration settings
    """
    DEBUG = False
    # TESTING = False
    # CSRF_ENABLED = True
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'bucketlist.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SECRET_KEY = os.urandom(24)

class DevelopmentConfig(Config):
    """
    Development configuration settings
    """
    DEBUG = True

class TestingConfig(Config):
    """
    Testing configuration settings
    """
    TESTING = True
    DEBUG = False

class ProductionConfig(Config):
    """
    Production configuration settings
    """
    DEBUG = False


configurations = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}