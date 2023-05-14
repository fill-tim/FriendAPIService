from rest_framework import generics

from .serializers import UserAuthenticationSerializer


# Create your views here.
class RegisterUserAPI(generics.CreateAPIView):
    serializer_class = UserAuthenticationSerializer

