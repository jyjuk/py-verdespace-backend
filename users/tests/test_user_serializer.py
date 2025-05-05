from django.test import TestCase
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer
from rest_framework.test import APIClient


class UserSerializerTests(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "user@example.com",
            "password": "testpass123",
            "username": "testuser",
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_create_user_serializer(self):
        data = {
            "email": "newuser@example.com",
            "password": "newpass123",
            "username": "newuser",
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.email, data["email"])
        self.assertTrue(user.check_password(data["password"]))

    def test_update_user_serializer(self):
        data = {"first_name": "Updated", "password": "newpass456"}
        serializer = UserSerializer(self.user, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        self.assertTrue(updated_user.check_password(data["password"]))

    def test_invalid_data_serializer(self):
        data = {
            "email": "valid@example.com",  # Дійсний email
            "password": "1234",  # Некоректний пароль (надто короткий)
            "username": "newuser",
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "password", serializer.errors
        )  # Очікуємо помилку для поля password

    def test_jwt_authorization(self):
        user = get_user_model().objects.create_user(
            email="jwtuser@example.com", password="testpass123"
        )
        client = APIClient()

        # Отримуємо токен
        token_response = client.post(
            "/api/user/token/",
            {"email": "jwtuser@example.com", "password": "testpass123"},
        )
        self.assertEqual(token_response.status_code, 200)

        access_token = token_response.data.get("access")
        print(f"Access Token: {access_token}")  # Додати для налагодження
        self.assertIsNotNone(access_token)

        # Використовуємо токен
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = client.get("/api/user/me/")
        print(f"Response: {response.data}")  # Додати для налагодження
        self.assertEqual(response.status_code, 200)
