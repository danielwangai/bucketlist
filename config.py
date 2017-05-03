"""To define configurations for different development environments."""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Common configuration settings
    """
    DEBUG = False
    # TESTING = False
    # CSRF_ENABLED = True
    # SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # environment variable for SECRET_KEY
    SECRET_KEY = os.environ['SECRET_KEY']


class DevelopmentConfig(Config):
    """
    Development configuration settings
    """
    DEBUG = True
    BASEURL = "http://127.0.0.1:5000/api/v1"


class TestingConfig(Config):
    """
    Testing configuration settings
    """
    basedir = os.path.abspath(os.path.dirname(__file__))

    TESTING = True
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # environment variable for SECRET_KEY
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir,
                                                           'bucketlist.db'))


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
