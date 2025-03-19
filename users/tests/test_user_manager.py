from django.test import TestCase
from django.contrib.auth import get_user_model


class UserManagerTests(TestCase):
    def test_create_user_with_email_successful(self):
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        email = "test@EXAMPLE.COM"
        user = get_user_model().objects.create_user(email, "test123")
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test123")

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            "super@example.com", "superpass123"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_email_uniqueness(self):
        email = "unique@example.com"
        password = "testpass123"
        get_user_model().objects.create_user(email=email, password=password)
        with self.assertRaises(Exception):
            get_user_model().objects.create_user(email=email, password=password)

    def test_username_auto_generated_from_email(self):
        email = "autouser@example.com"
        user = get_user_model().objects.create_user(email=email, password="testpass123")
        self.assertEqual(user.username, email)
