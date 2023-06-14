from django.http import HttpResponse
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers, models


# Create your views here.
class ListFriendsAPI(generics.ListAPIView):
    """ Вывод списка друзей пользователя """
    serializer_class = serializers.ListFriendsSerializer

    def get_queryset(self):
        queryset = models.Friend.objects.filter(user=self.request.user)
        return queryset


class OutgoingFriendRequests(generics.ListAPIView):
    """ Вывод списка исходящих запросов в друзья пользователя """
    serializer_class = serializers.OutgoingFriendRequestSerializer

    def get_queryset(self):
        queryset = models.FriendRequest.objects.filter(from_whom=self.request.user)
        return queryset


class IncomingFriendRequests(generics.ListAPIView):
    """ Вывод списка входящих запросов в друзья пользователя """
    serializer_class = serializers.IncomingFriendRequestSerializer

    def get_queryset(self):
        queryset = models.FriendRequest.objects.filter(to_whom=self.request.user)
        return queryset


class AddFriends(APIView):
    """ Добавление в друзья """

    def add_friend(self, *args, **kwargs):
        first_user = kwargs['from_whom']
        second_user = kwargs['to_whom']
        return self.add(first_user, second_user)

    def add(self, first_user, second_user):
        models.Friend.objects.create(user=first_user, friend=second_user)
        models.Friend.objects.create(user=second_user, friend=first_user)

        return {'message': 'Пользователь добавлен в друзья!', 'status': 201}


class GetObjectRequest:
    """ Возвращает объект "FriendRequest" """

    def get_obj_request(self, from_whom, to_whom):
        obj = models.FriendRequest.objects.filter(from_whom=from_whom, to_whom=to_whom)
        return obj


class DestroyMix(mixins.DestroyModelMixin):
    """ Для удаления объектов """

    def destroy(self, *args, **kwargs):
        obj = kwargs['obj']
        return self.perform_destroy(obj)


class RequestValidation(DestroyMix, GetObjectRequest, AddFriends):
    """ Проверка на входящий запрос в друзья """

    def request_validation(self, *args, **kwargs):
        from_whom = kwargs['from_whom']
        created_incoming = kwargs['created_incoming']
        to_whom = kwargs['to_whom']
        incoming_request = kwargs['incoming_request']
        return self.response(created_incoming, from_whom, to_whom, incoming_request)

    def response(self, created_incoming, from_whom, to_whom, incoming_request):
        if created_incoming:
            created_already = self.get_obj_request(from_whom=to_whom, to_whom=from_whom)
            if created_already.exists():
                response = self.add_friend(from_whom=from_whom, to_whom=to_whom)
                self.destroy(obj=incoming_request)
                self.destroy(obj=created_already)
                return response
            else:
                return {'message': 'Заявка отправлена!', 'status': 201}
        else:
            return {'message': 'Заявка уже была отправлена!', 'status': 200}


class GetUserObject:
    def get_obj_user(self, user):
        obj = models.User.objects.get(username=user)
        return obj


class RequestFriends(RequestValidation, GetUserObject):
    """ Отправка заявки в друзья пользователю """

    def post(self, request):
        from_whom = request.user
        to_whom = self.get_obj_user(self.request.data.get('username'))
        incoming_request, created_incoming = models.FriendRequest.objects.get_or_create(from_whom=from_whom,
                                                                                        to_whom=to_whom)
        response = self.request_validation(created_incoming=created_incoming, from_whom=from_whom,
                                           to_whom=to_whom, incoming_request=incoming_request)
        return Response(response)


class ResponseToRequest(AddFriends, DestroyMix):
    """ Ответ пользователя (принять/отклонить) на входящую заявку в друзья """

    def post(self, request):
        data = request.data
        obj = models.FriendRequest.objects.get(id=data['id'])
        if data['state'] == 'accept':
            response = self.add_friend(from_whom=obj.from_whom, to_whom=obj.to_whom)
            self.destroy(obj=obj)
            return Response(response)
        else:
            self.destroy(obj=obj)
            return Response({'message': 'Заявка отклонена!', 'status': 200})


class GetObjectFriend:
    """ Возвращает объект Friend """

    def get_obj_friend(self, user, friend):
        obj = models.Friend.objects.filter(user=user, friend=friend)
        return obj


class DeleteFriend(APIView, GetObjectFriend, DestroyMix):
    """ Удаление пользователя из друзей """

    def delete(self, request):
        id_num = request.data['id']
        obj_f = models.Friend.objects.get(id=id_num)
        obj_s = self.get_obj_friend(user=obj_f.friend, friend=obj_f.user)
        return self.destroy_request(obj_f, obj_s)

    def destroy_request(self, obj_f, obj_s):
        self.destroy(obj=obj_f)
        self.destroy(obj=obj_s)
        return Response({'message': 'Пользователь удален из друзей!'})


class DetectUsersState(APIView, GetObjectRequest, GetObjectFriend, GetUserObject):
    """ Определение связи между пользователями """

    def post(self, request):
        first_user = request.data.get('first_user')
        obj_first = self.get_obj_user(first_user)
        second_user = request.data.get('second_user')
        obj_second = self.get_obj_user(second_user)

        return self.detect_state(obj_first, obj_second)

    def detect_state(self, obj_first, obj_second):
        outgoing_request = self.get_obj_request(from_whom=obj_first, to_whom=obj_second)

        incoming_request = self.get_obj_request(from_whom=obj_second, to_whom=obj_first)

        friend = self.get_obj_friend(user=obj_first, friend=obj_second)

        return self.get_state(outgoing_request, incoming_request, friend)

    def get_state(self, outgoing_request, incoming_request, friend):
        if outgoing_request.exists():
            return Response({
                'message': f'Исходящая заявка от {outgoing_request.first().from_whom} пользователю {outgoing_request.get().to_whom}'
            })
        elif incoming_request.exists():
            return Response({
                'message': f'Входящая заявка от {incoming_request.first().from_whom} пользователю {incoming_request.get().to_whom}'
            })
        elif friend.exists():
            return Response({'message': 'Уже друзья'})
        else:
            return Response({'message': 'Ничего нет'})
