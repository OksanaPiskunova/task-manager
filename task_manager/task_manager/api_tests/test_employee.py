from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from task_manager.task_manager.models import Employee


EMPLOYEES_URL = '/employees/'
JSON = 'json'


class EmployeeTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username='user',
            email='user@man.com'
        )
        user.set_password('managerpassword')
        user.save()

        cls.manager = Employee.objects.get(user=user)
        cls.manager.role = Employee.MANAGER
        cls.manager.save()

    def test_post_employee(self):
        # Arrange
        client = APIClient()
        client.force_authenticate(user=self.manager)

        user = {
            'username': 'lilia',
            'email': 'lilia@lilia.lilia',
            'password': 'lilia'
        }
        employee = {
            'user': user,
            'role': 'Developer'
        }

        # Act
        response = client.post(EMPLOYEES_URL, employee)

        # Assert
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_get_employees(self):
        # Arrange
        client = APIClient()
        client.force_authenticate(user=self.manager)

        # Act
        response = client.get(EMPLOYEES_URL, format=JSON)

        # Assert
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['count'],
            1   # manager
        )

    def test_get_employee(self):
        # Arrange
        client = APIClient()
        client.force_authenticate(user=self.manager)

        url = '{0}1/'.format(EMPLOYEES_URL)

        # Act
        response = client.get(url, format=JSON)

        # Assert
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['role'],
            self.manager.role
        )

    def test_delete_employee(self):
        # Arrange
        client = APIClient()
        client.force_authenticate(user=self.manager)

        url = '{0}1/'.format(EMPLOYEES_URL)

        # Act
        response = client.delete(url)

        # Assert
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )