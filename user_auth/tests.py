from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAuthTest(APITestCase):

    def test_create_user(self):
        data = {'email': 'test@test.com', 'password': '22', 'password2': '22'}

        response = self.client.post(reverse('singup-api'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
