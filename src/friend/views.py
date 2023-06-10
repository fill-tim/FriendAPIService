from django.http import HttpResponse
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .models import Friend, User, FriendRequest
from .serializers import ListFriendsSerializer, IncomingFriendRequestSerializer, OutgoingFriendRequestSerializer


# Create your views here.
class ListFriendsAPI(generics.ListAPIView):
    """ Вывод списка друзей пользователя """
    serializer_class = ListFriendsSerializer

    def get_queryset(self):
        queryset = Friend.objects.filter(user=self.request.user)
        return queryset


class OutgoingFriendRequests(generics.ListAPIView):
    """ Вывод списка исходящих запросов в друзья пользователя """
    serializer_class = OutgoingFriendRequestSerializer

    def get_queryset(self):
        queryset = FriendRequest.objects.filter(to_whom=self.request.user)
        return queryset


class IncomingFriendRequests(generics.ListAPIView):
    """ Вывод списка входящих запросов в друзья пользователя """
    serializer_class = IncomingFriendRequestSerializer

    def get_queryset(self):
        queryset = FriendRequest.objects.filter(from_whom=self.request.user)
        return queryset


class AddFriends(APIView):
    """ Добавление в друзья """

    def add_friend(self, first_user, second_user):
        return self.add(first_user, second_user)

    def add(self, first_user, second_user):
        Friend.objects.create(user=first_user, friend=second_user)
        Friend.objects.create(user=second_user, friend=first_user)

        return HttpResponse('Пользователь добавлен в друзья!')


class DestroyRequests(APIView):
    """ Удаление заявок в друзья """
    def destroy_request(self, first_user, second_user):
        obj = FriendRequest.objects.get(from_whom=second_user, to_whom=first_user)
        return self.destroy(obj)

    def destroy(self, obj):
        return obj.delete()


class RequestFriend(DestroyRequests, AddFriends):
    """ Отправка заявки в друзья пользователю """

    def post(self, request):
        from_whom = self.request.user
        to_whom = User.objects.get(username=self.request.data.get('username'))
        incoming_request, created_incoming = FriendRequest.objects.get_or_create(from_whom=from_whom,
                                                                                 to_whom=to_whom)
        if created_incoming:
            created_already = FriendRequest.objects.filter(from_whom=to_whom, to_whom=from_whom).exists()
            if created_already:
                response = self.add_friend(from_whom, to_whom)
                self.destroy_request(from_whom, to_whom)
                self.destroy(incoming_request)
                return HttpResponse(response)
            else:
                return HttpResponse('Заявка отправлена!')
        else:
            return HttpResponse('Заявка уже была отправлена!')


class ResponseToRequest(AddFriends, DestroyRequests):
    """ Ответ пользователя (принять/отклонить) на входящую заявку в друзья """
    def post(self, request):
        data = self.request.data
        obj = FriendRequest.objects.get(id=data['id'])
        if data['state'] == 'accept':
            response = self.add_friend(first_user=obj.from_whom, second_user=obj.to_whom)
            self.destroy(obj)
            return HttpResponse(response)
        else:
            self.destroy(obj)
            return HttpResponse('Заявка отклонена!')
