"""Tests for API endpoints."""
import unittest
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
        response = self.client.get("/v1/bucketlists/")
        self.assertEqual(response.status_code, 200)

    def test_fetch_single_bucketlist(self):
        """Test that endpoint fetches a single bucketlist."""
        response = self.client.get('/v1/bucketlists/1/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
