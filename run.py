import os.path

from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api
from flask_script import Manager

from config import configurations  # QLALCHEMY_MIGRATE_REPO
from app import db, app
from app.models import User, Bucketlist, Item
from app.views import UserLogin, CreateUser, BucketlistResources


# app = Flask(__name__, instance_relative_config=True)
app.config.from_object(configurations["development"])
# add configuration settings from instance/config.py
app.config.from_pyfile('config.py')

db.init_app(app)

migrate = Migrate(app, db)

api = Api(app)

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


# api endpoints
api.add_resource(BucketlistResources, "/api/v1/bucketlists",
                 "/api/v1/bucketlists/<int:id>", endpoint='bucketlist')
api.add_resource(UserLogin, '/api/v1/auth/login', endpoint="login")
api.add_resource(CreateUser, '/api/v1/auth/register', endpoint="user_registration")

if __name__ == '__main__':
    # manager.run()
    app.run(debug=True, host='127.0.0.1', port=5000)
