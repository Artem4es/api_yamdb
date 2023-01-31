from django import views
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework.response import Response
from rest_framework import status, views
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.tokens import default_token_generator

from .serializers import UserSignUpSerializer, TokenSerializer
# Create your views here.

User = get_user_model()


class SignUpView(views.APIView):

    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=serializer.data['username'])
            confirmation_code = default_token_generator.make_token(user)
            print(confirmation_code)
            # тут будем письмо отсылать
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class TokenView(views.APIView):

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            try:
                user = get_object_or_404(User, username=username)
            except Http404:
                return Response(
                    'Пользователь с таким username не найдено',
                    status=status.HTTP_404_NOT_FOUND
                )
            if default_token_generator.check_token(
                    user, serializer.validated_data['confirmation_code']
            ):
                token = str(AccessToken.for_user(user))
                user_data = {
                    'username': user.username,
                    'token': token
                }
                return Response(user_data, status=status.HTTP_200_OK)
            return Response(
                'Указан неверный код подтверждения',
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





    ...

