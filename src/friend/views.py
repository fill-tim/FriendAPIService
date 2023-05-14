from rest_framework import generics

from .models import UserC, Friend
from .serializers import ListFriendsSerializer


# Create your views here.
class ListFriendsAPI(generics.ListAPIView):
    serializer_class = ListFriendsSerializer

    def get_queryset(self):
        user = self.request.user
        user_prof = UserC.objects.get(username=user.username)
        queryset = Friend.objects.filter(user=user)

        return queryset

