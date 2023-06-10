from rest_framework import serializers

from .models import User, Friend, FriendRequest


class UserProfileSerializer(serializers.ModelSerializer):
    """ Профиль пользователя """
    class Meta:
        model = User
        fields = '__all__'


class ListFriendsSerializer(serializers.ModelSerializer):
    """ Список друзей пользователя """
    friend = UserProfileSerializer(read_only=True)

    class Meta:
        model = Friend
        fields = ['friend']


class OutgoingFriendRequestSerializer(serializers.ModelSerializer):
    """ Исходящие запросы пользователя """
    to_user = UserProfileSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['to_whom']


class IncomingFriendRequestSerializer(serializers.ModelSerializer):
    """ Входящие запросы пользователя """
    to_user = UserProfileSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['from_whom']

