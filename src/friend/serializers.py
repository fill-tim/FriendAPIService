from rest_framework import serializers

from .models import UserC, Friend


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserC
#         fields = ['username']


class UserProfileSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)

    class Meta:
        model = UserC
        fields = '__all__'


class ListFriendsSerializer(serializers.ModelSerializer):
    friend = UserProfileSerializer(read_only=True)

    class Meta:
        model = Friend
        fields = ['friend']
