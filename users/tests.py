from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

""" 
    ENSURING THAT THE USERS ARE WELL REGISTERED
"""


class RegisterTestCase(APITestCase):

    def test_UserRegistration(self):
        data = {
            "username": "testcase",
            "email": "test@test.com",
            "password": "test123",
            "password2": "test123"
        }

        response = self.client.post(reverse('createUser'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


""" 
    ENSURING THAT THE USERS ARE WELL SIGNED IN AND OUT
"""


class LoginLogoutTestCase(APITestCase):

    def setUp(self):
        self.TestUser = User.objects.create_user(
            username="testAnon",
            password="test@123"
        )

    def test_Login(self):
        data = {
            "username": "testAnon",
            "password": "test@123"
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        self.token = Token.objects.get(user__username="testAnon")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
