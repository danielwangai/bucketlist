"""The entry point of the application."""

from app import create_app, api
from app.views import (UserLogin, CreateUser, BucketlistResources,
                       BucketlistItemResources)


app = create_app("development")

# api endpoints
api.add_resource(BucketlistResources, "/api/v1/bucketlists",
                 "/api/v1/bucketlists/<int:id>", endpoint='bucketlist')
api.add_resource(BucketlistItemResources,
                 "/api/v1/bucketlists/<int:bucketlist_id>/items",
                 "/api/v1/bucketlists/<int:bucketlist_id>/items/<int:item_id>",
                 endpoint='bucketlist_item')
api.add_resource(UserLogin, '/api/v1/auth/login', endpoint="login")
api.add_resource(CreateUser, '/api/v1/auth/register', endpoint="user_registration")

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
