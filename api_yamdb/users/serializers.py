from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from .models import User


class UserSignUpSerializer(serializers.Serializer):

    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[UnicodeUsernameValidator(), ]
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )

    def validate(self, data):
        """
        Валидация полей при регистрации пользователя.
        1) Username "me" запрещен
        2) Неуникальный username запрещен
        3) Неуникальный email запрещен
        """
        username = data.get('username')
        email = data.get('email')
        if username == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать "me" в качестве имени пользователя.'
            )
        if User.objects.filter(username=username, email=email).exists():
            return data
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Другой пользователь с таким username уже существует.'
            )
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Другой пользователь с таким email уже существует.'
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UserIsMeSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role', )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
