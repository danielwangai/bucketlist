"""The entry point of the application."""

from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api
from flask_script import Manager

from config import configurations
from app import db, create_app, api
from app.models import User, Bucketlist, Item
from app.views import UserLogin, CreateUser, BucketlistResources


app = create_app(configurations["development"])

# api endpoints
api.add_resource(BucketlistResources, "/api/v1/bucketlists",
                 "/api/v1/bucketlists/<int:id>", endpoint='bucketlist')
api.add_resource(UserLogin, '/api/v1/auth/login', endpoint="login")
api.add_resource(CreateUser, '/api/v1/auth/register', endpoint="user_registration")

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
