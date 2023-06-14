from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from src.friend.models import User


class RegisterTestCase(APITestCase):
    """ Тестирование регистрации """
    def test_registration(self):
        data = {"username": "Fill", "password": "1234"}
        response = self.client.post(reverse("register"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
