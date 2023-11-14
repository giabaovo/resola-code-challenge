from django.test import TestCase

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import User


class UserModelTest(TestCase):

    def test_create_user(self):
        User.objects.create_user("test@gmail.com", "123456")
        user = User.objects.get(email="test@gmail.com")

        self.assertEqual(str(user), "test@gmail.com")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_super_user(self):
        User.objects.create_superuser("test@gmail.com", "123456")
        user = User.objects.get(email="test@gmail.com")

        self.assertEqual(str(user), "test@gmail.com")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_raise_error_when_no_email_supplied(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="123456")


class RegisterAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = "/api/account/register/"

    def test_register_user(self):
        user_data = {
            "email": "test@gmail.com",
            "password": "123456",
        }

        response = self.client.post(self.register_url, data=user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(User.objects.filter(email=user_data["email"]).exists())

        expected_response_data = {
            "status": f"User register with email {user_data['email']} successfully"
        }
        self.assertEqual(response.json(), expected_response_data)

    def test_register_user_invalid_data(self):
        invalid_user_data = {
            "email": "invalidemail",
            "password": "weak",
        }

        response = self.client.post(self.register_url, data=invalid_user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("email", response.json())


class LoginAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = "/api/account/login/"
        self.user_data = {
            "email": "test@gmail.com",
            "password": "123456",
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_login_valid_credentials(self):
        response = self.client.post(self.login_url, data=self.user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("token", response.json())

    def test_login_invalid_credentials(self):
        invalid_user_data = {
            "email": "test@example.com",
            "password": "wrongpassword",
        }

        response = self.client.post(self.login_url, data=invalid_user_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertIn("error", response.json())

class LogoutAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.logout_url = "/api/account/logout/"
        self.user_data = {
            "email": "test@example.com",
            "password": "securepassword123",
        }
        User.objects.create_user(**self.user_data)
        self.user = User.objects.get(email="test@example.com")
        self.token, _ = Token.objects.get_or_create(user=self.user)

    def test_logout_authenticated_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_logout_unauthenticated_user(self):
        response = self.client.post(self.logout_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertIn("detail", response.json())