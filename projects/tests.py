from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from projects.views import CreateProjectView, RetrieveUpdateDeleteProjectView
from users.models import User
from .models import Project


class ProjectTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username="bob", email="bob@mail.com", password="password"
        )

    def test_project_create(self):
        view = CreateProjectView().as_view()
        url = reverse("project_create")

        user_mike = User.objects.create_user(
            username="mike", email="mike@mail.com", password="password"
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
        view = CreateProjectView().as_view()
        url = reverse("project_create")

        Project.objects.create(
            owner=self.user, name="First Project", description="My first project"
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
            owner=self.user, name="First Project", description="My first project"
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
            owner=self.user, name="First Project", description="My first project"
        )

        request = self.factory.delete(url, format="json")
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)

        self.assertEqual(response.status_code, 204, response.data)
