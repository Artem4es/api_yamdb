from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserSignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email'
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    confirmation_code = serializers.CharField(max_length=100)
