from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import RegisterUser
from .models import User


class UserTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username="bob", email="bob@mail.com", password="password"
        )

    def test_register(self):
        view = RegisterUser.as_view()

        data = {
            "username": "test_user",
            "email": "test-user@mail.com",
            "password": "1234",
        }
        request = self.factory.post("/api/users/register/", data, format="json")
        response = view(request)

        self.assertEqual(response.status_code, 201, response.data)

    def test_register_existing_email(self):
        view = RegisterUser.as_view()

        data = {
            "username": "test_user",
            "email": "bob@mail.com",  # Existing email
            "password": "password",
        }
        request = self.factory.post("/api/users/register/", data, format="json")
        response = view(request)

        self.assertEqual(response.status_code, 400, response.data)

    def test_register_non_valid_email(self):
        view = RegisterUser.as_view()

        data = {
            "username": "test_user",
            "email": "not-an-email",  # Invalid email
            "password": "password",
        }
        request = self.factory.post("/api/users/register/", data, format="json")
        response = view(request)

        self.assertEqual(response.status_code, 400, response.data)

    def test_register_existing_username(self):
        view = RegisterUser.as_view()

        data = {
            "username": "bob",  # Existing username
            "email": "test@mail.com",
            "password": "password",
        }
        request = self.factory.post("/api/users/register/", data, format="json")
        response = view(request)

        self.assertEqual(response.status_code, 400, response.data)

    def test_login(self):
        view = TokenObtainPairView.as_view()

        data = {
            "username": "bob",
            "password": "password",
        }
        request = self.factory.post("/api/users/login/", data, format="json")
        response = view(request)

        self.assertEqual(response.status_code, 200, response.data)

        # Test Refresh Token
        data = response.data

        view = TokenRefreshView.as_view()
        request = self.factory.post("/api/users/token/refresh/", data, format="json")
        response = view(request)

        self.assertEqual(response.status_code, 200, response.data)

    def test_login_fail(self):
        view = TokenObtainPairView.as_view()

        data = {
            "username": "not_bob",
            "password": "password",
        }
        request = self.factory.post("/api/users/login/", data, format="json")
        response = view(request)

        self.assertEqual(response.status_code, 401, response.data)
