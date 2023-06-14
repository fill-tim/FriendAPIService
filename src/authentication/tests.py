from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from src.friend.models import User


class RegisterTestCase(APITestCase):
    def test_create_account(self):
        url = reverse('register')
        response = self.client.get(url)
        print(response)
