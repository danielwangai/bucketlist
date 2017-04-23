import json
import unittest

from app import create_app, api, db
from app.views import UserLogin, CreateUser, BucketlistResources


class BaseTestCase(unittest.TestCase):
    """Test for API endpoints."""

    def create_app(self):
        app = create_app('testing')
        return app

    def setUp(self):
        """To declare test-wide variables."""

        self.app = self.create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        # set api endpoints
        api.add_resource(BucketlistResources, "/api/v1/bucketlists",
                         "/api/v1/bucketlists/<int:id>", endpoint='bucketlist')
        api.add_resource(UserLogin, '/api/v1/auth/login', endpoint="login")
        api.add_resource(CreateUser, '/api/v1/auth/register', endpoint="user_registration")

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
