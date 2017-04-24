import json
from app.models import Bucketlist, Item, User

from tests import BaseTestCase


class APIEndpointsTestCase(BaseTestCase):
    """Test for API endpoints."""

    def test_fetch_all_bucketlists(self):
        """Test that endpoint fetches all bucketlists."""
        # create bucketlist
        new_bucketlist = {
            "name": "Crack Game theory."
        }
        response = self.client.post('/api/v1/bucketlists', data=new_bucketlist,
                                    headers=self.headers)
        self.assertEqual(json.loads(response.data)["msg"],
                         "Bucketlist created successfully.")
        self.assertEqual(response.status_code, 201)
        # fetch bucketlists
        response = self.client.get("/api/v1/bucketlists",
                                   headers=self.headers
                                   )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)["msg"],
                         "Fetched all my bucketlists.")

    def test_fetch_single_bucketlist(self):
        """Test that endpoint fetches a single bucketlist."""
        new_bucketlist = {
            "name": "Crack Game theory."
        }
        response = self.client.post('/api/v1/bucketlists', data=new_bucketlist,
                                    headers=self.headers)
        self.assertEqual(json.loads(response.data)["msg"],
                         "Bucketlist created successfully.")
        self.assertEqual(response.status_code, 201)
        # fetch single bucketlist
        response = self.client.get('/api/v1/bucketlists/1',
                                   headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)["msg"],
                         "Bucketlist fetched successfully")

    def test_post_new_bucketlist(self):
        """Test endpoint saves new bucketlist."""
        new_bucketlist = {
            "name": "Crack Game theory."
        }
        response = self.client.post('/api/v1/bucketlists', data=new_bucketlist,
                                    headers=self.headers)
        self.assertEqual(json.loads(response.data)["msg"],
                         "Bucketlist created successfully.")
        self.assertEqual(response.status_code, 201)

    def test_recreate_bucketlist(self):
        """Test endpoint rejects creating existing bucketlist."""
        response = self.client.post('/api/v1/bucketlists', data=self.bucket_1,
                                    headers=self.headers)
        self.assertEqual(json.loads(response.data)["msg"],
                         "Bucketlist created successfully.")
        self.assertEqual(response.status_code, 201)
        # attempts recreating the same bucketlist
        response = self.client.post('/api/v1/bucketlists', data=self.bucket_1,
                                    headers=self.headers)
        self.assertEqual(json.loads(response.data)["error"],
                         "The bucketlist already exists")
        self.assertEqual(response.status_code, 409)

    def test_update_bucketlist(self):
        """Test endpoint updates bucketlist."""
        bucketlist = {
            "name": "Crack Game theory."
        }
        # create bucketlist
        response = self.client.post('/api/v1/bucketlists', data=bucketlist,
                                    headers=self.headers
                                    )
        self.assertEqual(json.loads(response.data)["msg"],
                         "Bucketlist created successfully."
                         )
        self.assertEqual(response.status_code, 201)
        # update bucketlist
        bucket_update = {
            "name": "Crack Game theory, updated."
        }
        response = self.client.put('/api/v1/bucketlists/1', data=bucket_update,
                                   headers=self.headers
                                   )
        self.assertEqual(json.loads(response.data)["msg"],
                         "Update successful."
                         )
        self.assertEqual(response.status_code, 200)

    def test_can_only_update_own_bucket(self):
        """Test user can only update own bucket."""
        bucketlist = {
            "name": "Crack Game theory."
        }
        # create bucketlist
        response = self.client.post('/api/v1/bucketlists', data=bucketlist,
                                    headers=self.headers
                                    )
        self.assertEqual(json.loads(response.data)["msg"],
                         "Bucketlist created successfully."
                         )
        self.assertEqual(response.status_code, 201)
        # update bucketlist
        bucket_update = {
            "name": "Crack Game theory, updated."
        }
        response = self.client.put('/api/v1/bucketlists/1', data=bucket_update,
                                   headers=self.headers_2
                                   )
        self.assertEqual(json.loads(response.data)["error"],
                         "You can only update your own bucketlist."
                         )
        self.assertEqual(response.status_code, 400)

    def test_update_inexistent_bucket(self):
        """Test endpoint rejects updating inexistent bucketlist."""
        bucket_update = {
            "name": "Crack Game theory, updated."
        }
        response = self.client.put('/api/v1/bucketlists/12345',
                                   data=bucket_update, headers=self.headers
                                   )
        self.assertEqual(json.loads(response.data)["error"],
                         "Buckelist of given id does not exist."
                         )
        self.assertEqual(response.status_code, 404)

    def test_reject_update_with_same_name(self):
        """Test endpoint updates bucketlist."""
        bucketlist = {
            "name": "Crack Game theory."
        }
        # create bucketlist
        response = self.client.post('/api/v1/bucketlists', data=bucketlist,
                                    headers=self.headers
                                    )
        self.assertEqual(json.loads(response.data)["msg"],
                         "Bucketlist created successfully."
                         )
        self.assertEqual(response.status_code, 201)
        # update bucketlist
        bucket_update = {
            "name": "Crack Game theory."
        }
        response = self.client.put('/api/v1/bucketlists/1', data=bucket_update,
                                   headers=self.headers
                                   )
        self.assertEqual(json.loads(response.data)["error"],
                         "Cannot update bucket with same name."
                         )
        self.assertEqual(response.status_code, 409)

    def test_update_bucketlist_with_empty_values(self):
        """Test endpoint updates bucketlist."""
        bucketlist = {
            "name": "Crack Game theory."
        }
        # create bucketlist
        response = self.client.post('/api/v1/bucketlists', data=bucketlist,
                                    headers=self.headers
                                    )
        self.assertEqual(json.loads(response.data)["msg"],
                         "Bucketlist created successfully."
                         )
        self.assertEqual(response.status_code, 201)
        # update bucketlist
        bucket_update = {
            "name": ""
        }
        response = self.client.put('/api/v1/bucketlists/1', data=bucket_update,
                                   headers=self.headers
                                   )
        self.assertEqual(json.loads(response.data)["error"],
                         "Cannot update to empty value."
                         )
        self.assertEqual(response.status_code, 400)

    def test_delete_bucketlist(self):
        """Test endpoint deletes bucketlist."""
        bucketlist = {
            "name": "Crack Game theory."
        }
        # create bucketlist
        response = self.client.post('/api/v1/bucketlists', data=bucketlist,
                                    headers=self.headers
                                    )
        self.assertEqual(json.loads(response.data)["msg"],
                         "Bucketlist created successfully."
                         )
        self.assertEqual(response.status_code, 201)
        # delete bucketlist
        response = self.client.delete('/api/v1/bucketlists/1',
                                      data=bucketlist, headers=self.headers
                                      )
        self.assertEqual(json.loads(response.data)["msg"],
                         "Bucket deletion success."
                         )
        self.assertEqual(response.status_code, 200)

    def test_delete_inexistent_bucketlist(self):
        """Test reject deleting inexistent bucketlist."""
        bucketlist = {
            "name": "Crack Game theory."
        }
        # create bucketlist
        response = self.client.post('/api/v1/bucketlists', data=bucketlist,
                                    headers=self.headers
                                    )
        self.assertEqual(json.loads(response.data)["msg"],
                         "Bucketlist created successfully."
                         )
        self.assertEqual(response.status_code, 201)
        # attempt delete
        response = self.client.delete('/api/v1/bucketlists/1234',
                                      data=bucketlist, headers=self.headers
                                      )
        self.assertEqual(json.loads(response.data)["error"],
                         "Bucket does not exist."
                         )
        self.assertEqual(response.status_code, 404)

    def test_only_delete_own_bucketlist(self):
        """Test user can only delete own bucketlist."""
        bucketlist = {
            "name": "Crack Game theory."
        }
        # create bucketlist
        response = self.client.post('/api/v1/bucketlists', data=bucketlist,
                                    headers=self.headers
                                    )
        self.assertEqual(json.loads(response.data)["msg"],
                         "Bucketlist created successfully."
                         )
        self.assertEqual(response.status_code, 201)
        # delete bucketlist
        response = self.client.delete('/api/v1/bucketlists/1',
                                      headers=self.headers_2
                                      )
        self.assertEqual(json.loads(response.data)["error"],
                         "Can only delete your own backetlist."
                         )
        self.assertEqual(response.status_code, 400)

    def test_user_login_authenticates_valid_credentials(self):
        """Test that endpoint authenticates valid credentials."""
        response = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'username': 'dan',
                'password': 'password123'}),
            content_type='application/json')
        self.assertEqual(200, response.status_code)
        # confirm that token is in response
        self.assertIn("Authorization", response.data.decode("ascii"))
        self.assertEqual(self.token,
                         json.loads(response.data)["Authorization"])

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
