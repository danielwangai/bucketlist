import unittest
# local imports
from app import db, app


class APIEndpointsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.app_context()
        self.client = app.test_client()

    def test_fetch_all_bucketlists(self):
        response = self.client.get("/v1/bucketlists/")
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
