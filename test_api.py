"""Tests for API endpoints."""
import unittest
import json

# local imports
from app import app


class APIEndpointsTestCase(unittest.TestCase):
    """Test for API endpoints."""

    def setUp(self):
        """Test wide variables."""
        self.app = app.app_context()
        self.client = app.test_client()

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
        response = self.client.post('/api/v1/bucketlists', data=json.dumps(
            new_bucketlist))
        self.assertEqual(response.status_code, 201)

    def test_update_bucketlist(self):
        """Test endpoint updates bucketlist."""
        bucketlist = {
            "name": "Crack Game theory, updated."
        }
        response = self.client.post('/api/v1/bucketlists/1',
                                    data=json.dumps(bucketlist))
        self.assertEqual(response.status_code, 200)

    def test_delete_bucketlist(self):
        """Test endpoint deletes bucketlist."""
        bucketlist = {
            "name": "Crack Game theory, updated."
        }
        response = self.client.delete('/api/v1/bucketlists/1',
                                      data=json.dumps(bucketlist))
        self.assertEqual(response.status_code, 200)

    def test_login_rejects_invalid_params(self):
        """Test that endpoint rejects invalid params."""
        user = {
            "invalid1": "dan",
            "invalid2": "password123"
        }
        response = self.client.post('/api/v1/auth/login', data=json.dumps(
            user))
        # bad request
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
