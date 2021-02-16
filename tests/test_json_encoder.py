from unittest import TestCase
import json

from app import ContactAwareJSONEncoder
from app import Contact


class TestContactAwareJSONEncoder(TestCase):
    def test_default(self):
        """ContactAwareJSONEncoder should correctly encode Contact model"""

        contact = Contact("Test user", "user@test.com", 1234567890)
        result = json.dumps(contact, cls=ContactAwareJSONEncoder)

        expected_result = '{"name": "Test user", "email": "user@test.com", "number": 1234567890}'
        self.assertEqual(result, expected_result)
