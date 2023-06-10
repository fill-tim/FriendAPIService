from rest_framework import generics

from .serializers import UserAuthenticationSerializer
from django.contrib.auth.hashers import make_password


# Create your views here.
class RegisterUserAPI(generics.CreateAPIView):
    serializer_class = UserAuthenticationSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()
