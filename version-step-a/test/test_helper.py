import unittest
from utils.helper import Sanitizer

class TestSanitizer(unittest.TestCase):
    def test_get_valid_name(self):
        # Test valid name
        sanitizer = Sanitizer("John Doe")
        self.assertEqual(sanitizer.get_valid_name(), "John Doe")

        # Test invalid name with special characters
        sanitizer = Sanitizer("John@Doe")
        self.assertIsNone(sanitizer.get_valid_name())

    def test_get_valid_username(self):
        # Test valid username
        sanitizer = Sanitizer("johndoe_123")
        self.assertEqual(sanitizer.get_valid_username(), "johndoe_123")

        # Test invalid username with spaces
        sanitizer = Sanitizer("john doe")
        self.assertIsNone(sanitizer.get_valid_username())

    def test_get_valid_email(self):
        # Test valid email
        sanitizer = Sanitizer("john.doe@example.com")
        self.assertEqual(sanitizer.get_valid_email(), "john.doe@example.com")

        # Test invalid email without domain
        sanitizer = Sanitizer("john.doe")
        self.assertIsNone(sanitizer.get_valid_email())

    def test_get_valid_phone(self):
        # Test valid phone number
        sanitizer = Sanitizer("+1234567890")
        self.assertEqual(sanitizer.get_valid_phone(), "+1234567890")

        # Test invalid phone number with alphabets
        sanitizer = Sanitizer("123abc")
        self.assertIsNone(sanitizer.get_valid_phone())

    def test_get_valid_location(self):
        # Test valid location
        sanitizer = Sanitizer("New York")
        self.assertEqual(sanitizer.get_valid_location(), "New York")

        # Test invalid location with numbers
        sanitizer = Sanitizer("London 123")
        self.assertIsNone(sanitizer.get_valid_location())
