"""To initialize the application."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__, instance_relative_config=True)

db = SQLAlchemy()


def create_app(config_name):
    # create flask object
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_name)
    # add configuration settings from instance/config.py
    app.config.from_pyfile('config.py')
    db.init_app(app)

    migrate = Migrate(app, db)

    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    return app
