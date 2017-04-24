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

    def test_cannot_invalid_bucketlist_id(self):
        """To test that endpoint rejects item with invalid bucketlist_id."""
        response = self.client.post('/api/v1/bucketlists/111/items',
                                    data=dict(name="another bucket item"),
                                    headers=self.headers
                                    )
        self.assertEqual(json.loads(response.data)["error"],
                         "Invalid bucketlist id."
                         )
        self.assertEqual(response.status_code, 404)

    def test_update_item_successfully(self):
        """To test that endpoint updates successfully."""
        # create an item
        response = self.client.post('/api/v1/bucketlists/1/items',
                                    data=self.bucket_item,
                                    headers=self.headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)["msg"],
                         "Bucket item created successfully.")
        # update item
        response = self.client.put('/api/v1/bucketlists/1/items/1',
                                   data={"name": "update"},
                                   headers=self.headers)
        self.assertEqual(json.loads(response.data)["msg"],
                         "Item update successful."
                         )
        self.assertEqual(response.status_code, 200)
