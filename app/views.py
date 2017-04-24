from flask import g
from flask_httpauth import HTTPTokenAuth
from flask_restful import Resource, reqparse

from app import db
from app.models import Bucketlist, Item, User

# create instance of HTTPTokenAuth
auth = HTTPTokenAuth(scheme="Token")


@auth.verify_token
def verify_token(token):
    """To validate the token sent by the user."""
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True


class UserLogin(Resource):
    """Class to authenticate a user."""

    def __init__(self):
        """To add for arguments login endpoint."""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str,
                                   help='Username required', required=True)
        self.reqparse.add_argument('password', type=str,
                                   help='Password required', required=True)

    def post(self):
        """To authenticate a user."""
        args = self.reqparse.parse_args()
        if not args['username'] or not args['password']:
            return {'msg': 'Please provide all credentials'}, 400
        else:
            user = User.query.filter_by(username=args['username']).first()
            if user:
                token = user.generate_auth_token()
                return {'Authorization': 'Token ' + token.decode('ascii')}, 200
            else:
                return {"msg": "invalid username password combination"}, 401


class CreateUser(Resource):
    """Class to create a user."""

    def __init__(self):
        """To add for arguments user registration endpoint."""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str,
                                   help='Username required', required=True)
        self.reqparse.add_argument('password', type=str,
                                   help='Password required', required=True)

    def post(self):
        """To create a new user."""
        args = self.reqparse.parse_args()
        if not args['username'] or not args['password']:
            return {'error': 'Username and password required'}, 400
        else:
            if len(args['password']) < 8:
                return ({'error':
                         'Password must be atleast 8 characters long!'
                         }, 400)
            else:
                if User.query.filter_by(username=args['username']).first():
                    # if user with given username exists
                    return ({
                        'error': 'A User with the same name already exists!'},
                        409)
                user = User(username=args['username'],
                            password=args['password'])
                db.session.add(user)
                db.session.commit()
                return {'success': 'User Registration success!'}, 201


class BucketlistResources(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str,
                                   help='Wrong key', required=True)

    def get(self, id=None):
        """To return bucketlist(s)."""
        pass

    @auth.login_required
    def post(self):
        """To create a new bucketlist."""
        args = self.reqparse.parse_args()

        return self.validate_create_bucket_list(args)

    def validate_create_bucket_list(self, data):
        """To alidate details required for bucket list creation."""
        values = ["name"]

        for value in values:
            if data.get(value).isspace() or not data.get(value):
                return {'error': 'Invalid parameter.'}, 400

        if Bucketlist.query.filter_by(name=data["name"]).first():
            return {'error': 'The bucketlist already exists'}, 409

        bucketlist = Bucketlist(name=data["name"])
        db.session.add(bucketlist)
        db.session.commit()
        return {"msg": "Bucketlist created successfully.",
                "bucket": bucketlist.to_json()}, 201

    def put(self, id):
        """To update a bucketlist."""
        pass

    def delete(self, id):
        """To delete a bucketlist."""
        pass


class BucketlistItemResources(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str,
                                   help='The key name required.',
                                   required=True)

    def get(self, id=None):
        """To return task(s)."""
        pass

    def post(self):
        """To create a new item."""
        pass

    def put(self, id):
        """To update an item."""
        pass

    def delete(self, id):
        """To delete an item."""
        pass
