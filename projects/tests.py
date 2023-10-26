from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from projects.views import (
    CreateApplicationView,
    ListCreateProjectView,
    RetrieveUpdateDeleteProjectView,
)
from users.models import User
from .models import Application, Project


class ProjectTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username="bob",
            email="bob@mail.com",
            password="password",
        )

    def test_project_create(self):
        view = ListCreateProjectView().as_view()
        url = reverse("project_list_create")

        user_mike = User.objects.create_user(
            username="mike",
            email="mike@mail.com",
            password="password",
        )
        data = {
            "name": "First Project",
            "description": "My first project",
            "collaborators": [user_mike.id],
        }
        request = self.factory.post(url, data, format="json")
        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code, 201, response.data)

    def test_project_create_duplicate(self):
        view = ListCreateProjectView().as_view()
        url = reverse("project_list_create")

        Project.objects.create(
            owner=self.user,
            name="First Project",
            description="My first project",
        )

        data = {"name": "First Project"}
        request = self.factory.post(url, data, format="json")
        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code, 400, response.data)

    def test_project_patch(self):
        view = RetrieveUpdateDeleteProjectView().as_view()
        url = reverse("project_get_update_delete", kwargs={"pk": 1})

        Project.objects.create(
            owner=self.user,
            name="First Project",
            description="My first project",
        )

        data = {"completed": True}
        request = self.factory.patch(url, data, format="json")
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)

        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data.get("completed"), True, response.data)

    def test_project_delete(self):
        view = RetrieveUpdateDeleteProjectView().as_view()
        url = reverse("project_get_update_delete", kwargs={"pk": 1})

        Project.objects.create(
            owner=self.user,
            name="First Project",
            description="My first project",
        )

        request = self.factory.delete(url, format="json")
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)

        self.assertEqual(response.status_code, 204, response.data)


class ApplicationTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username="bob",
            email="bob@mail.com",
            password="password",
        )
        self.demo_project = Project.objects.create(name="Demo Project", owner=self.user)

    def test_application_create(self):
        view = CreateApplicationView().as_view()
        url = reverse("application_create")

        user_mike = User.objects.create_user(
            username="mike",
            email="mike@mail.com",
            password="password",
        )
        data = {"project": self.demo_project.id}
        request = self.factory.post(url, data, format="json")
        force_authenticate(request, user=user_mike)
        response = view(request)

        self.assertEqual(response.status_code, 201, response.data)

    def test_application_by_project_owner(self):
        view = CreateApplicationView().as_view()
        url = reverse("application_create")

        data = {"project": self.demo_project.id}
        request = self.factory.post(url, data, format="json")
        force_authenticate(request, user=self.user)
        response = view(request)

        self.assertEqual(response.status_code, 400, response.data)

    def test_application_create_duplicate(self):
        view = CreateApplicationView().as_view()
        url = reverse("application_create")

        user_mike = User.objects.create_user(
            username="mike",
            email="mike@mail.com",
            password="password",
        )
        Application.objects.create(user=user_mike, project=self.demo_project)

        data = {"project": self.demo_project.id}
        request = self.factory.post(url, data, format="json")
        force_authenticate(request, user=user_mike)
        response = view(request)

        self.assertEqual(response.status_code, 400, response.data)
