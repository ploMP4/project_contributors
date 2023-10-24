from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import DeleteSkillView, RegisterUserView, CreateSkillView
from .models import Language, Level, Skill, User


class UserTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username="bob", email="bob@mail.com", password="password"
        )

    def test_register(self):
        view = RegisterUserView.as_view()
        url = reverse("register")

        data = {
            "username": "test_user",
            "email": "test-user@mail.com",
            "password": "1234",
        }
        request = self.factory.post(url, data, format="json")
        response = view(request)

        self.assertEqual(response.status_code, 201, response.data)

    def test_register_existing_email(self):
        view = RegisterUserView.as_view()
        url = reverse("register")

        data = {
            "username": "test_user",
            "email": "bob@mail.com",  # Existing email
            "password": "password",
        }
        request = self.factory.post(url, data, format="json")
        response = view(request)

        self.assertEqual(response.status_code, 400, response.data)

    def test_register_non_valid_email(self):
        view = RegisterUserView.as_view()
        url = reverse("register")

        data = {
            "username": "test_user",
            "email": "not-an-email",  # Invalid email
            "password": "password",
        }
        request = self.factory.post(url, data, format="json")
        response = view(request)

        self.assertEqual(response.status_code, 400, response.data)

    def test_register_existing_username(self):
        view = RegisterUserView.as_view()
        url = reverse("register")

        data = {
            "username": "bob",  # Existing username
            "email": "test@mail.com",
            "password": "password",
        }
        request = self.factory.post(url, data, format="json")
        response = view(request)

        self.assertEqual(response.status_code, 400, response.data)

    def test_login(self):
        view = TokenObtainPairView.as_view()
        url = reverse("login")

        data = {
            "username": "bob",
            "password": "password",
        }
        request = self.factory.post(url, data, format="json")
        response = view(request)

        self.assertEqual(response.status_code, 200, response.data)

        # Test Refresh Token
        view = TokenRefreshView.as_view()
        url = reverse("token_refresh")

        data = response.data
        request = self.factory.post(url, data, format="json")
        response = view(request)

        self.assertEqual(response.status_code, 200, response.data)

    def test_login_fail(self):
        view = TokenObtainPairView.as_view()
        url = reverse("login")

        data = {
            "username": "not_bob",
            "password": "password",
        }
        request = self.factory.post(url, data, format="json")
        response = view(request)

        self.assertEqual(response.status_code, 401, response.data)


class SkillTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username="bob", email="bob@mail.com", password="password"
        )

    def test_skill_create(self):
        view = CreateSkillView.as_view()
        url = reverse("skill")

        data = {"language": Language.PYTHON, "level": Level.EXPERIENCED}

        request = self.factory.post(url, data, format="json")
        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code, 201, response.data)

    def test_skill_create_unauthenticated(self):
        view = CreateSkillView.as_view()
        url = reverse("skill")

        data = {"language": "python", "level": "experienced"}

        request = self.factory.post(url, data, format="json")
        response = view(request)

        self.assertEqual(response.status_code, 401, response.data)

    def test_skill_create_not_available_language(self):
        view = CreateSkillView.as_view()
        url = reverse("skill")

        data = {"language": "random-language", "level": "expert"}

        request = self.factory.post(url, data, format="json")
        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code, 400, response.data)

    def test_skill_create_not_available_level(self):
        view = CreateSkillView.as_view()
        url = reverse("skill")

        # Try creating a skill with a different level than the ones available
        data = {"language": "python", "level": "really good"}

        request = self.factory.post(url, data, format="json")
        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code, 400, response.data)

    def test_skill_create_duplicate(self):
        view = CreateSkillView.as_view()
        url = reverse("skill")

        Skill.objects.create(
            user=self.user, language=Language.PYTHON, level=Level.EXPERIENCED
        )

        data = {"language": Language.PYTHON, "level": Level.EXPERT}

        request = self.factory.post(url, data, format="json")
        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code, 400, response.data)

    def test_skill_create_more_that_three(self):
        view = CreateSkillView.as_view()
        url = reverse("skill")

        Skill.objects.create(
            user=self.user, language=Language.PYTHON, level=Level.EXPERIENCED
        )
        Skill.objects.create(
            user=self.user, language=Language.GO, level=Level.EXPERIENCED
        )
        Skill.objects.create(
            user=self.user, language=Language.RUST, level=Level.BEGINNER
        )

        data = {"language": Language.CPP, "level": Level.EXPERT}

        request = self.factory.post(url, data, format="json")
        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code, 400, response.data)

    def test_skill_delete(self):
        view = DeleteSkillView.as_view()
        url = reverse("skill_delete", kwargs={"pk": 1})

        Skill.objects.create(
            user=self.user, language=Language.PYTHON, level=Level.EXPERIENCED
        )

        request = self.factory.delete(url, format="json")
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)

        self.assertEqual(response.status_code, 204, response.data)
