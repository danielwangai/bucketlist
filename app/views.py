"""Define api endpoints and logic."""
from urllib.parse import urljoin

from flask import g
from flask_httpauth import HTTPTokenAuth
from flask_restful import Resource, reqparse

from app import db, api
from app.models import Bucketlist, Item, User
from config import configurations

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
    """To perform CRUD on Bucetlists."""

    def __init__(self):
        """To define bucket params."""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str,
                                   help='Wrong key', required=True)
        self.reqparse.add_argument('description', type=str, help='Wrong key')

    @auth.login_required
    def get(self, id=None):
        """To return bucketlist(s)."""
        # add arguments for search and limits
        parser = reqparse.RequestParser()
        parser.add_argument(
            'limit', type=int, help='Limit must be a number',
            required=False, location='args')
        parser.add_argument(
            'q', type=str, help='Query must be a string',
            required=False, location='args')
        parser.add_argument("page", type=int, required=False, location='args')
        args = parser.parse_args()
        if id:
            bucketlist = Bucketlist.query.filter_by(id=id).first()
            if bucketlist:
                if bucketlist.created_by == g.user.id:
                    # if bucket list was created by current user
                    return {"id": bucketlist.id,
                            "name": bucketlist.name,
                            "created_at": str(bucketlist.created_at),
                            "modified_at": str(bucketlist.modified_at),
                            "created_by": bucketlist.created_by,
                            "items": [{
                                "id": item.id,
                                "name": item.name,
                                "done": item.done
                            }
                                for item in bucketlist.items]
                            }, 200
                else:
                    return (
                        {"error": "Bucketlist not found."},
                        404)
            else:
                return {"error": "Bucketlist not found."}, 404
        else:
            if args["page"] or args["limit"]:
                bucketlists = (Bucketlist.query.filter_by(
                    created_by=g.user.id).paginate(page=args["page"],
                                                   per_page=args["limit"],
                                                   error_out=False))
                my_buckets = []
                next_url = None
                prev_url = None
                if bucketlists:
                    for bucketlist in bucketlists.items:
                        my_buckets.append({
                            "id": bucketlist.id,
                            "name": bucketlist.name,
                            "created_at": str(bucketlist.created_at),
                            "modified_at": str(bucketlist.modified_at),
                            "created_by": bucketlist.created_by,
                            "items": [{
                                "id": item.id,
                                "name": item.name,
                                "done": item.done
                            }
                                for item in bucketlist.items],
                        })
                    if bucketlists.has_next:
                        next_url = (urljoin(
                            configurations["development"].BASEURL +
                            "/bucketlists", api.url_for(
                                BucketlistResources,
                                page=bucketlists.next_num,
                                limit=bucketlists.per_page)))
                    if bucketlists.has_prev:
                        prev_url = (urljoin(
                            configurations["development"].BASEURL +
                            "/bucketlists", api.url_for(
                                BucketlistResources,
                                page=bucketlists.prev_num,
                                limit=bucketlists.per_page)))
                    page_details = {
                        "current_page": bucketlists.page,
                        "limit": 2,
                        "next_page": next_url,
                        "prev_page": prev_url,
                        "bucketlists": my_buckets
                    }
                    return page_details, 200
                else:
                    return {"error": "You have no bucketlists"}, 404

            elif args["q"]:
                # serches
                bucketlists = (Bucketlist.query.filter(
                    Bucketlist.name.like('%{}%'.format(
                        args['q'].lower()))).filter_by(
                    created_by=int(str(g.user.id))).all())

                if bucketlists:
                    results = []
                    for bucketlist in bucketlists:
                        results.append({
                            "id": bucketlist.id,
                            "name": bucketlist.name,
                            "created_at": str(bucketlist.created_at),
                            "modified_at": str(bucketlist.modified_at),
                            "created_by": bucketlist.created_by,
                            "items": [{
                                "id": item.id,
                                "name": item.name,
                                "done": item.done
                            }
                                for item in bucketlist.items]
                        })

                    return results, 200
                else:
                    return ({"error":
                             "There is no bucketlist containing that name."},
                            404)
            else:
                # get bucketlists for all users
                bucketlists = Bucketlist.query.filter_by(created_by=g.user.id)
                my_buckets = []
                if bucketlists:
                    for bucketlist in bucketlists:
                        my_buckets.append({
                            "id": bucketlist.id,
                            "name": bucketlist.name,
                            "created_at": str(bucketlist.created_at),
                            "modified_at": str(bucketlist.modified_at),
                            "created_by": bucketlist.created_by,
                            "items": [{
                                "id": item.id,
                                "name": item.name,
                                "done": item.done
                            }
                                for item in bucketlist.items],
                        })
                return my_buckets, 200

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

        if Bucketlist.query.filter_by(name=data["name"].lower(),
                                      created_by=g.user.id).first():
            return {'error': 'The bucketlist already exists'}, 409

        bucketlist = Bucketlist(name=data["name"].lower(),
                                created_by=g.user.id)
        db.session.add(bucketlist)
        db.session.commit()
        return {"msg": "Bucketlist created successfully.",
                "bucket": bucketlist.to_json()}, 201

    @auth.login_required
    def put(self, id):
        """To update a bucketlist."""
        bucket = Bucketlist.query.filter_by(id=id).first()
        args = self.reqparse.parse_args()

        if not bucket:
            return {"error": "Buckelist of given id does not exist."}, 404

        if args["name"]:
            if bucket.created_by == g.user.id:
                if Bucketlist.query.filter_by(
                        name=args["name"].lower()).first():
                    # check if bucket with same name exists
                    return ({"error": "Cannot update bucket with same name."},
                            409)
                else:
                    bucket.name = args["name"]
                    db.session.add(bucket)
                    db.session.commit()
                    return {"msg": "Update successful."}, 200
            else:
                return ({"error": "You can only update your own bucketlist."},
                        400)
        else:
            return {"error": "Cannot update to empty value."}, 400

    @auth.login_required
    def delete(self, id):
        """To delete a bucketlist."""
        # fetch bucket
        bucket = Bucketlist.query.filter_by(id=id).first()
        if bucket:
            if bucket.created_by == g.user.id:
                # bucket exists
                db.session.delete(bucket)
                db.session.commit()
                return ({'msg': 'Bucket deletion success.'}, 200)
            elif bucket.created_by != g.user.id:
                return {"error": "Can only delete your own backetlist."}, 400
        else:
            return ({'error': 'Bucket does not exist.'}, 404)


class BucketlistItemResources(Resource):
    """To perform CRUD on Bucetlist Items."""

    def __init__(self):
        """To define bucketlist item params."""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str,
                                   help='The key name required.')
        self.reqparse.add_argument('status', type=str,
                                   help='status of the item')

    @auth.login_required
    def get(self, bucketlist_id, item_id=None):
        """To return task(s)."""
        bucketlist = Bucketlist.query.get(bucketlist_id)

        if not bucketlist:
            return (
                {"error": "Cannot fetch items with invalid bucketlist id."},
                404)
        # reject unauthorized access
        if bucketlist:
            # fetch all bucketlists
            if not item_id:
                items = []
                for item in bucketlist.items:
                    items.append({"id": item.id, "name": item.name,
                                  "status": item.done})
                return items, 200
            if item_id:
                item = Item.query.get(item_id)
                if item:
                    return {"id": item.id, "name": item.name,
                            "status": item.done}, 200
                else:
                    return (
                        {"error":
                         "Invalid Item id. Item not found."},
                        404)

    @auth.login_required
    def post(self, bucketlist_id):
        """To create a new item."""
        args = self.reqparse.parse_args()
        bucketlist = Bucketlist.query.get(bucketlist_id)
        # for invalid bucketlist id
        if not bucketlist:
            return {"error": "Bucketlist of given ID does not exist."}, 404
        # prevent unauthorized access
        if bucketlist.created_by != g.user.id:
            return {"error": "Unathorized Access!"}, 403

        # search if item with current name exists
        bucketlist_item = Item.query.filter_by(name=args['name']).first()
        if bucketlist_item:
            return {"error": "Cannot create duplicate item names."}, 409

        if not args["name"]:
            return {"error": "Must set item name."}, 400

        bucketlist_id = bucketlist.id
        item = Item(name=args['name'],
                    done=False,
                    bucketlist_id=bucketlist_id)
        db.session.add(item)
        db.session.commit()

        return {"msg": "Bucket item created successfully."}, 201

    @auth.login_required
    def put(self, bucketlist_id, item_id):
        """To update an item."""
        args = self.reqparse.parse_args()
        bucketlist = Bucketlist.query.get(bucketlist_id)
        item = Item.query.get(item_id)
        if not bucketlist:
            return {"error": "Invalid bucketlist id."}, 404
        # prevent unauthorized access
        if bucketlist.created_by != g.user.id:
            return {"error": "Unauthorized update rejected."}, 403

        if item:
            if args["status"] in ["True", "true"]:
                item.name = args["name"] or item.name
                item.done = True
                db.session.commit()
                return {"msg": "Item update successful."}, 200
            elif args["status"] in ["False", "false"]:
                if args["name"]:
                    if item.name == args["name"]:
                        return {"error": "Cannot update with same name."}, 400
                    else:
                        item.name = args["name"] or item.name
                        item.done = False
                        db.session.commit()
                        return {"msg": "Item update successful."}, 200
                else:
                    return {"error": "Cannot update with empty name."}, 400
            else:
                return {"error": "Status should be True or False"}, 400

        elif not item:
            return {"error": "Invalid item id."}, 404

    @auth.login_required
    def delete(self, bucketlist_id, item_id):
        """To delete an item."""
        # fetch bucketlist
        bucketlist = Bucketlist.query.filter_by(id=bucketlist_id).first()

        # Retrieve the item
        item = Item.query.filter_by(id=item_id).first()

        if not bucketlist:
            return {"error": "Invalid bucketlist id."}, 404
        # prevent unauthorized access
        if bucketlist.created_by != g.user.id:
            return {"error": "Unauthorized deltion rejected."}, 403

        if not item:
            return {"error": "Item not found."}, 404

        db.session.delete(item)
        db.session.commit()

        return {"msg": "Item deletion successful."}, 200
