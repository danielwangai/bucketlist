import os.path
import unittest

from db import create_db

class DBCommandTestCase(unittest.TestCase):
    def test_create_db_can_create_database(self):
        """To test that create_db can create database."""
        create_db()
        self.assertTrue(os.path.exists("bucketlist.db"))

if __name__ == '__main__':
    unittest.main()