from flask import g
from flask_restful import Resource, reqparse

from app import db
from app.models import Bucketlist, Item, User


class UserLogin(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParse()
        self.reqparse.add_argument('username', type=str,
                                   help='Username required', required=True)
        self.reqparse.add_argument('password', type=str,
                                   help='Password required', required=True)

    def post(self):
        pass


class CreateUser(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, help='Username required', required=True)
        self.reqparse.add_argument('password', type=str, help='Password required', required=True)

    def post(self):
        pass


class BucketlistResources(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, help='Wrong key', required=True)
        self.reqparse.add_argument('description', type=str,
                                   help='description cannot be blank', required=True)

    def get(self, id=None):
        """To return bucketlist(s)."""
        pass

    def post(self):
        """To create a new bucketlist."""
        pass

    def put(self, id):
        """To update a bucketlist."""
        pass

    def delete(self, id):
        """To delete a bucketlist."""
        pass
