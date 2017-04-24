"""To test bucketlist item endpoints."""
import json

from app.models import Bucketlist, Item, User
from tests import BaseTestCase


class BucketlistItemTestCase(BaseTestCase):
    """Tests for bucketlist items."""

    def test_endpoint_creates_item(self):
        """Test that endpoint creates an item."""
        response = self.client.post('/api/v1/bucketlists/1/items',
                                    data=self.bucket_item,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)["msg"],
                         "Bucket item created successfully.")

    def test_reject_similar_item_name(self):
        """To test that endpoint rejects similar bucketlist name."""
        response = self.client.post('/api/v1/bucketlists/1/items',
                                    data=self.bucket_item,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)["msg"],
                         "Bucket item created successfully.")

        response = self.client.post('/api/v1/bucketlists/1/items',
                                    data=self.bucket_item,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(json.loads(response.data)["error"],
                         "Cannot create duplicate item names."
                         )

    def test_reject_empty_item_name(self):
        """To test that endpoint rejects item with empty name."""
        response = self.client.post('/api/v1/bucketlists/1/items',
                                    data=dict(name=""),
                                    headers=self.headers
                                    )
        self.assertEqual(json.loads(response.data)["error"],
                         "Must set item name."
                         )
        self.assertEqual(response.status_code, 400)
