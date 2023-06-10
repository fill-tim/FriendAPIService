from rest_framework import serializers

from src.friend.models import User


class UserAuthenticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
