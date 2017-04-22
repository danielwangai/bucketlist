"""The entry point of the application."""

from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api
from flask_script import Manager

from config import configurations
from app import db, create_app
from app.models import User, Bucketlist, Item
from app.views import UserLogin, CreateUser, BucketlistResources


app = create_app(configurations["development"])

if __name__ == '__main__':
    # manager.run()
    app.run(debug=True, host='127.0.0.1', port=5000)
