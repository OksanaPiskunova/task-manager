from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User


USERS_URL = '/users/'
JSON = 'json'


class UserTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create(
            username='admin',
            email='admin@admin.com'
        )
        cls.admin.is_staff = True
        cls.admin.set_password('adminpassword')
        cls.admin.save()

    def test_post_user(self):
        # Arrange
        client = APIClient()
        client.force_authenticate(user=self.admin)

        username = 'Petr'
        user = {
            'username': username,
            'email': 'petr@petr.petr',
            'password': 'petr'
        }

        # Act
        response = client.post(USERS_URL, user, format=JSON)

        # Assert
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            User.objects.count(),
            2   # user + admin
        )
        self.assertEqual(
            User.objects.get(username=username).username,
            username
        )

    def test_get_users(self):
        # Arrange
        client = APIClient()
        client.force_authenticate(user=self.admin)

        # Act
        response = client.get(USERS_URL, format=JSON)

        # Assert
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['count'],
            1   # admin
        )

    def test_get_user(self):
        # Arrange
        client = APIClient()
        client.force_authenticate(user=self.admin)

        url = '{0}1/'.format(USERS_URL)

        # Act
        response = client.get(url, format=JSON)

        # Assert
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['username'],
            self.admin.username
        )

    def test_put_user(self):
        # Arrange
        client = APIClient()
        client.force_authenticate(user=self.admin)

        email_field = 'email'
        new_email = 'new@admin.com'
        url = '{0}1/'.format(USERS_URL)

        # Act
        response = client.put(
            url,
            {
                'id': self.admin.id,
                'username': self.admin.username,
                'password': 'petr',
                email_field: new_email
            }
        )

        # Assert
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data[email_field],
            new_email
        )

    def test_delete_user(self):
        # Arrange
        client = APIClient()
        client.force_authenticate(user=self.admin)

        url = '{0}1/'.format(USERS_URL)

        # Act
        response = client.delete(url)

        # Assert
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
