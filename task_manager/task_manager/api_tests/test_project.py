from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from task_manager.task_manager.models import Employee, Project


EMPLOYEES_URL = '/employees/'
PROJECTS_URL = '/projects/'
JSON = 'json'


class ProjectTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create manager
        manager_user = User.objects.create(
            username='manager_user',
            email='manager@user.com'
        )
        manager_user.set_password('managerpassword')
        manager_user.save()

        cls.manager = Employee.objects.get(user=manager_user)
        cls.manager.role = Employee.MANAGER
        cls.manager.save()

        # Create developer
        developer_user = User.objects.create(
            username='developer_user',
            email='developer@user.com'
        )
        developer_user.set_password('developerpassword')
        developer_user.save()

        cls.developer = Employee.objects.get(user=developer_user)
        cls.developer.role = Employee.DEVELOPER
        cls.developer.save()

        # Create project
        cls.project = Project.objects.create()
        cls.project.title = 'Project'
        cls.project.description = 'Description'
        cls.project.managers = [
            cls.manager,
        ]
        cls.project.developers = [
            cls.developer,
        ]
        cls.project.save()

    def test_post_project(self):
        # Arrange
        client = APIClient()
        client.force_authenticate(user=self.manager)

        project = {
            'title': 'Project',
            'description': 'Project description',
            'managers': [
                '{0}{1}/'.format(
                    EMPLOYEES_URL,
                    self.manager.id
                ),
            ],
            'developers': [
                '{0}{1}/'.format(
                    EMPLOYEES_URL,
                    self.developer.id
                ),
            ]
        }

        # Act
        response = client.post(PROJECTS_URL, project, format=JSON)

        # Assert
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            Project.objects.count(),
            2   # initial project + this project
        )

    def test_get_projects(self):
        # Arrange
        client = APIClient()
        client.force_authenticate(user=self.manager)

        # Act
        response = client.get(PROJECTS_URL, format=JSON)

        # Assert
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['count'],
            1
        )

    def test_get_project(self):
        # Arrange
        client = APIClient()
        client.force_authenticate(user=self.manager)

        url = '{0}1/'.format(PROJECTS_URL)

        # Act
        response = client.get(url, format=JSON)

        # Assert
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['title'],
            self.project.title
        )

    def test_put_project(self):
        # Arrange
        client = APIClient()
        client.force_authenticate(user=self.manager)

        description_field = 'description'
        new_description = 'NEW NEW NEW NEW NEW'
        project = {
            'title': 'Project',
            description_field: new_description,
            'managers': [
                '{0}{1}/'.format(
                    EMPLOYEES_URL,
                    self.manager.id
                ),
            ],
            'developers': [
                '{0}{1}/'.format(
                    EMPLOYEES_URL,
                    self.developer.id
                ),
            ]
        }

        url = '{0}1/'.format(PROJECTS_URL)

        # Act
        response = client.put(url, project, format=JSON)

        # Assert
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data[description_field],
            new_description
        )

    def test_delete_project(self):
        # Arrange
        client = APIClient()
        client.force_authenticate(user=self.manager)

        url = '{0}1/'.format(PROJECTS_URL)

        # Act
        response = client.delete(url)

        # Assert
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )