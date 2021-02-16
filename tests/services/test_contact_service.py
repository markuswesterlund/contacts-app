import json
import os
import tempfile
from unittest import TestCase

from app import ContactAwareJSONEncoder
from app import Contact
from app import ContactService


class TestContactService(TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(mode="w", delete=False)
        self.temp_db_name = self.temp_db.name

        self.test_contact = Contact("Test User", "user@test.com", 1234567890)

        json.dump([self.test_contact], self.temp_db, indent=2, cls=ContactAwareJSONEncoder)
        self.temp_db.seek(0)

        self.contact_service = ContactService(self.temp_db_name)

    def tearDown(self):
        os.unlink(self.temp_db_name)

    def test_get_count(self):
        self.assertTrue(self.contact_service.get_count(), 1)

    def test_get_contacts(self):
        contacts = self.contact_service.get_contacts()

        self.assertEqual(contacts[0].name, self.test_contact.name)

    def test_create(self):
        pass

    def test_update(self):
        pass

    def test_remove(self):
        pass
