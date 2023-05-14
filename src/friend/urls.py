from django.urls import path

from .views import ListFriendsAPI

urlpatterns = [
    path('list/', ListFriendsAPI.as_view())
]
