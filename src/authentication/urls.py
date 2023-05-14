from django.urls import path

from .views import RegisterUserAPI

urlpatterns = [
    path('register/', RegisterUserAPI.as_view()),
]
