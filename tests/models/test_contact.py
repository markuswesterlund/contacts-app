from unittest import TestCase

from app import Contact


class TestContact(TestCase):
    """The contact model tests"""

    def setUp(self):
        self.name = "Test user"
        self.email = "user@test.com"
        self.number = 1234567890
        self.contact = Contact(self.name, self.email, self.number)

    def test_structure(self):
        """Contact model should have all required fields"""
        self.assertEqual(self.contact.name, self.name)
        self.assertEqual(self.contact.email, self.email)
        self.assertEqual(self.contact.number, self.number)

    def test_to_dict(self):
        expected_result = {"name": self.name, "email": self.email, "number": self.number}
        self.assertDictEqual(self.contact.to_dict(), expected_result)

    def test_get_display_value(self):
        expected_result = f"{self.name} / {self.email} / {self.number}"
        self.assertEqual(self.contact.get_display_value(), expected_result,
                         "Expected to have display value as <name> / <email> / <number> ")

    def test_has_email(self):
        self.assertTrue(self.contact.has_email())
