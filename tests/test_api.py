import json
from app.models import Bucketlist, Item, User

from tests import BaseTestCase


class APIEndpointsTestCase(BaseTestCase):
    """Test for API endpoints."""

    def test_fetch_all_bucketlists(self):
        """Test that endpoint fetches all bucketlists."""
        response = self.client.get("/api/v1/bucketlists")
        self.assertEqual(response.status_code, 200)

    def test_fetch_single_bucketlist(self):
        """Test that endpoint fetches a single bucketlist."""
        response = self.client.get('/api/v1/bucketlists/1')
        self.assertEqual(response.status_code, 200)

    def test_post_new_bucketlist(self):
        """Test endpoint saves new bucketlist."""
        new_bucketlist = {
            "name": "Crack Game theory."
        }
        response = self.client.post('/api/v1/bucketlists', data=new_bucketlist)
        self.assertEqual(response.status_code, 201)

    def test_update_bucketlist(self):
        """Test endpoint updates bucketlist."""
        bucketlist = {
            "name": "Crack Game theory, updated."
        }
        response = self.client.put('/api/v1/bucketlists/1', data=bucketlist)
        self.assertEqual(response.status_code, 200)

    def test_delete_bucketlist(self):
        """Test endpoint deletes bucketlist."""
        bucketlist = {
            "name": "Crack Game theory, updated."
        }
        response = self.client.delete('/api/v1/bucketlists/1', data=bucketlist)
        self.assertEqual(response.status_code, 200)

    def test_login_rejects_invalid_params(self):
        """Test that endpoint rejects invalid params."""
        user = {
            "invalid1": "dan",
            "invalid2": "password123"
        }
        response = self.client.post('/api/v1/auth/login', data=user)
        # bad request
        self.assertEqual(response.status_code, 400)

    def test_user_login_with_empty_fields(self):
        """Test that endpoint rejects authenticating user with empty fields."""
        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'username': '',
                'password': ''}),
            content_type='application/json')
        self.assertEqual('Please provide all credentials',
                         json.loads(response.data)['msg'])
        self.assertEqual(response.status_code, 400)

    def test_user_login_reject_invalid_credentials(self):
        """Test that endpoint authenticating rejects invalid credentials."""
        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'username': 'invalid1',
                'password': 'invalid2'}),
            content_type='application/json')
        self.assertEqual('invalid username password combination',
                         json.loads(response.data)['msg'])
        self.assertEqual(401, response.status_code)

    def test_create_user_rejects_invalid_params(self):
        """Test that endpoint rejects invalid params."""
        user = {
            "invalid1": "dan",
            "invalid2": "password123"
        }
        response = self.client.post('/api/v1/auth/register', data=user)
        # bad request
        self.assertEqual(response.status_code, 400)

    def test_endpoint_creates_user(self):
        """Test that endpoint creates user successfully."""
        new_user = {
            "username": "maina",
            "password": "password123"
        }
        response = self.client.post('/api/v1/auth/register', data=new_user)
        # status CREATED
        self.assertEqual(response.status_code, 201)

    def test_endpoint_rejects_duplicate_username(self):
        """Test that endpoint rejects creating duplicate usernames."""
        new_user = {
            "username": "dan",
            "password": "password123"
        }
        response = self.client.post('/api/v1/auth/register', data=new_user)
        # duplicate record found
        self.assertEqual(response.status_code, 409)
        self.assertEqual("A User with the same name already exists!",
                         json.loads(response.data)["error"]
                         )

    def test_endpoint_reject_short_password(self):
        """Test that endpoint rejects creating user with short password."""
        new_user = {
            "username": "dan",
            "password": "short"
        }
        response = self.client.post('/api/v1/auth/register', data=new_user)
        self.assertEqual("Password must be atleast 8 characters long!",
                         json.loads(response.data)["error"]
                         )
        self.assertEqual(response.status_code, 400)

    def test_endpoint_reject_create_user_with_empty_fields(self):
        """Test that endpoint rejects creating user with empty fields."""
        new_user = {
            "username": "",
            "password": ""
        }
        response = self.client.post('/api/v1/auth/register', data=new_user)
        self.assertEqual("Username and password required",
                         json.loads(response.data)["error"]
                         )
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
