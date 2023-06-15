from django.urls import path

from . import views

urlpatterns = [
    path('list_friends/', views.ListFriendsAPI.as_view(), name="list_friends"),
    path('outgoing_request/', views.OutgoingFriendRequests.as_view(), name='outgoing_request'),
    path('incoming_request/', views.IncomingFriendRequests.as_view(), name='incoming_request'),
    path('send_request/', views.RequestFriends.as_view(), name='send_request',),
    path('response_to_request/', views.ResponseToRequest.as_view(), name="response_to_request"),
    path('delete_friend/', views.DeleteFriend.as_view(), name="delete_friend"),
    path('detect_user_state/', views.DetectUsersState.as_view(), name="detect_users_state"),
]
