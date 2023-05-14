from rest_framework import serializers

from src.friend.models import UserC


class UserAuthenticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserC
        fields = ['username', 'password']
