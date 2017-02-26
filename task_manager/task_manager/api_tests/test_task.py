from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from task_manager.task_manager.models import Employee, Project, Task
import datetime

EMPLOYEES_URL = '/employees/'
PROJECTS_URL = '/projects/'
TASKS_URL = '/tasks/'
JSON = 'json'


class TaskTests(APITestCase):
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

        # Create task
        cls.task = Task.objects.create(
            project=cls.project,
            assigned_employee=cls.developer,
            due_date=datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        )
        cls.task.title = 'Task#1'
        cls.task.description = 'Description'
        cls.task.type = Task.BUG
        cls.task.status = Task.TO_DO
        cls.task.save()

    def test_post_task(self):
        # Arrange
        client = APIClient()
        client.force_authenticate(user=self.manager)

        task = {
            'title': 'Task#4',
            'description': 'Task description',
            'project': '{0}{1}/'.format(
                PROJECTS_URL,
                self.project.id
            ),
            'assigned_employee': '{0}{1}/'.format(
                EMPLOYEES_URL,
                self.manager.id
            ),
            'due_date': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            'type': Task.FEATURE,
            'status': Task.IN_PROGRESS
        }

        # Act
        response = client.post(TASKS_URL, task, format=JSON)

        # Assert
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            Task.objects.count(),
            2  # initial task + this task
        )

    def test_get_tasks(self):
        # Arrange
        client = APIClient()
        client.force_authenticate(user=self.manager)

        # Act
        response = client.get(TASKS_URL, format=JSON)

        # Assert
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['count'],
            1
        )

    def test_get_task(self):
        # Arrange
        client = APIClient()
        client.force_authenticate(user=self.manager)

        url = '{0}1/'.format(TASKS_URL)

        # Act
        response = client.get(url, format=JSON)

        # Assert
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['title'],
            self.task.title
        )

    def test_put_task(self):
        # Arrange
        client = APIClient()
        client.force_authenticate(user=self.manager)

        description_field = 'description'
        new_description = 'Task description'
        task = {
            'title': 'Task#1',
            description_field: new_description,
            'project': '{0}{1}/'.format(
                PROJECTS_URL,
                self.project.id
            ),
            'assigned_employee': '{0}{1}/'.format(
                EMPLOYEES_URL,
                self.manager.id
            ),
            'due_date': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            'type': Task.FEATURE,
            'status': Task.IN_PROGRESS
        }

        url = '{0}1/'.format(TASKS_URL)

        # Act
        response = client.put(url, task, format=JSON)

        # Assert
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data[description_field],
            new_description
        )

    def test_delete_task(self):
        # Arrange
        client = APIClient()
        client.force_authenticate(user=self.manager)

        url = '{0}1/'.format(TASKS_URL)

        # Act
        response = client.delete(url)

        # Assert
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
