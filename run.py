import os.path

from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from config import configurations  # QLALCHEMY_MIGRATE_REPO
from app import db
from app.models import User, Bucketlist, Task


app = Flask(__name__, instance_relative_config=True)
app.config.from_object(configurations["development"])
# add configuration settings from instance/config.py
app.config.from_pyfile('config.py')

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    """To manually create db."""
    if os.path.exists(configurations["development"].SQLALCHEMY_MIGRATE_REPO):
        print("Database already exists.")
    else:
        db.create_all()
        print("Database successfully created.")


@manager.command
def drop_db():
    """Management command to drop db."""
    db.drop_all()


if __name__ == '__main__':
    manager.run()
