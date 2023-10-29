import json
import random
from typing import Any
from faker import Faker
import requests

USER_COUNT = 10
PROJECT_PER_USER = 5
APPLICATIONS_PER_PROJECT = 5

BASE_URL = "http://127.0.0.1:8000/api"


class Factory:
    fake: Faker
    users: list[dict[Any, Any]]
    projects: list[dict[Any, Any]]

    def __init__(self, fake: Faker) -> None:
        self.fake = fake
        self.users = []
        self.projects = []

    def generate_data(self):
        self.create_users()
        self.create_user_skills()
        self.create_projects()
        self.create_applications()

    def create_users(self) -> None:
        for _ in range(USER_COUNT):
            user_data = {
                "first_name": self.fake.unique.first_name(),
                "last_name": self.fake.unique.last_name(),
                "age": random.randint(18, 45),
                "country": self.fake.unique.country(),
                "residence": self.fake.unique.address(),
            }
            user_data["username"] = user_data["first_name"][0] + user_data["last_name"]
            user_data["email"] = user_data["username"] + "@mail.com"
            user_data["password"] = user_data["username"] + "123"

            response = requests.post(f"{BASE_URL}/user/register/", data=user_data)
            user = json.loads(response.content.decode())
            self.users.append(user)

    def create_user_skills(self) -> None:
        level = ["beginner", "experienced", "expert"]
        language = ["C++", "javascript", "python", "java", "lua", "rust", "go", "julia"]

        for user in self.users:
            for _ in range(random.randint(1, 3)):
                skill_data = {
                    "level": random.choice(level),
                    "language": random.choice(language),
                }

                requests.post(
                    f"{BASE_URL}/user/skill/",
                    data=skill_data,
                    headers={"Authorization": "Bearer " + user["token"]["access"]},
                )

    def create_projects(self) -> None:
        for user in self.users:
            for _ in range(PROJECT_PER_USER):
                project_data = {
                    "name": self.fake.unique.word(),
                    "description": self.fake.text(),
                    "maximum_collaborators": random.randint(1, 5),
                    "collaborators": [],
                }

                for _ in range(
                    random.randint(0, project_data["maximum_collaborators"])
                ):
                    random_user = random.choice(self.users)
                    while random_user["id"] == user["id"]:
                        random_user = random.choice(self.users)

                    project_data["collaborators"].append(random_user["id"])

                response = requests.post(
                    f"{BASE_URL}/project/",
                    data=project_data,
                    headers={"Authorization": "Bearer " + user["token"]["access"]},
                )
                project = json.loads(response.content.decode())
                self.projects.append(project)

    def create_applications(self) -> None:
        for project in self.projects:
            for _ in range(APPLICATIONS_PER_PROJECT):
                application_data = {"project": project["id"]}

                user = random.choice(self.users)
                while user["username"] == project["creator"]:
                    user = random.choice(self.users)

                requests.post(
                    f"{BASE_URL}/project/application/",
                    data=application_data,
                    headers={"Authorization": "Bearer " + user["token"]["access"]},
                )


if __name__ == "__main__":
    f = Factory(Faker())
    f.generate_data()
