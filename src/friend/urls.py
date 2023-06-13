from django.urls import path

from . import views

urlpatterns = [
    path('list_friends/', views.ListFriendsAPI.as_view()),
    path('outgoing_request/', views.OutgoingFriendRequests.as_view()),
    path('incoming_request/', views.IncomingFriendRequests.as_view()),
    path('send_request/', views.RequestFriends.as_view()),
    path('response_to_request/', views.ResponseToRequest.as_view()),
    path('delete_friend/', views.DeleteFriend.as_view()),
    path('detect_user_state/', views.DetectUsersState.as_view()),
]
