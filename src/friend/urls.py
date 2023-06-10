from django.urls import path

from .views import ListFriendsAPI, RequestFriend, IncomingFriendRequests, OutgoingFriendRequests, ResponseToRequest

urlpatterns = [
    path('list_friends/', ListFriendsAPI.as_view()),
    path('outgoing_request/', OutgoingFriendRequests.as_view()),
    path('incoming_request/', IncomingFriendRequests.as_view()),
    path('send_request/', RequestFriend.as_view()),
    path('response_to_request/', ResponseToRequest.as_view()),
]
