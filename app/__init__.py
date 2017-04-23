"""To initialize the application."""

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api

from config import configurations

# initialize api blueprint
api_blueprint = Blueprint('api', __name__)
# initialize the api class
api = Api(api_blueprint)

db = SQLAlchemy()


def create_app(config_name):
    # create flask object
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(configurations[config_name])
    # add configuration settings from instance/config.py
    app.config.from_pyfile('config.py')
    db.init_app(app)
    app.register_blueprint(api_blueprint)

    migrate = Migrate(app, db)

    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    return app
