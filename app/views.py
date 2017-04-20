from flask import g
from flask_restful import Resource, reqparse

from app import db, app
from app.models import Bucketlist, Task, User


class UserLogin(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParse()
        self.reqparse.add_argument('username', type=str,
                                   help='Username required', required=True)
        self.reqparse.add_argument('password', type=str,
                                   help='Password required', required=True)

    def post(self):
        pass
