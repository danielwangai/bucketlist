from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__, instance_relative_config=True)
# app.config.from_object(configurations["development"])
# # add configuration settings from instance/config.py
# app.config.from_pyfile('config.py')

db = SQLAlchemy()

from app.models import User, Bucketlist, Item
