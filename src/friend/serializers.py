from rest_framework import serializers

from . import models


class UserProfileSerializer(serializers.ModelSerializer):
    """ Профиль пользователя """
    class Meta:
        model = models.User
        fields = '__all__'


class ListFriendsSerializer(serializers.ModelSerializer):
    """ Список друзей пользователя """
    friend = UserProfileSerializer(read_only=True)

    class Meta:
        model = models.Friend
        fields = ['friend']


class OutgoingFriendRequestSerializer(serializers.ModelSerializer):
    """ Исходящие запросы пользователя """
    to_user = UserProfileSerializer(read_only=True)

    class Meta:
        model = models.FriendRequest
        fields = ['to_whom']


class IncomingFriendRequestSerializer(serializers.ModelSerializer):
    """ Входящие запросы пользователя """
    to_user = UserProfileSerializer(read_only=True)

    class Meta:
        model = models.FriendRequest
        fields = ['from_whom']

