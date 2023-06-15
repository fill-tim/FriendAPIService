from django.urls import path, include, re_path

from .views import RegisterUserAPI

urlpatterns = [
    path('register/', RegisterUserAPI.as_view(), name="register"),
    path('auth/', include('djoser.urls')),
    re_path('auth/', include('djoser.urls.authtoken')),
]
