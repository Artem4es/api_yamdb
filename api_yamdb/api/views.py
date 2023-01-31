from django.conf import settings
from django import views
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import filters, viewsets, status, views

from reviews.models import Review, Title, Category, Genre, Title

from .permissions import (
    AdminOrReadOnly,
    AuthorAdminModeratorPermission,
    IsAdmin,
    IsSuperUser
)
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitlePostSerializer,
    CommentSerializer,
    ReviewSerializer,
    UserSignUpSerializer,
    TokenSerializer,
)


from api.custom_viewsets import (
    CreateReadDeleteModelViewSet,
    CreateReadUpdateDeleteModelViewset,
)


User = get_user_model()


class CategoryViewSet(CreateReadDeleteModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = [AdminOrReadOnly, ]


class GenreViewSet(CreateReadDeleteModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = [AdminOrReadOnly, ]


class TitleViewSet(CreateReadUpdateDeleteModelViewset):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')
    permission_classes = [AdminOrReadOnly, ]

    def get_serializer_class(self):
        if self.action in ('create', 'patch'):
            return TitlePostSerializer
        return TitleSerializer


class SignUpView(views.APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=serializer.data['username'])
            confirmation_code = default_token_generator.make_token(user)
            print(confirmation_code)
            send_mail(
                subject='Код подтверждения',
                message=f'Ваш код: {confirmation_code}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email, ]
            )
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class TokenView(views.APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            try:
                user = get_object_or_404(User, username=username)
            except Http404:
                return Response(
                    'Пользователь с таким username не найдено',
                    status=status.HTTP_404_NOT_FOUND,
                )
            if default_token_generator.check_token(
                user, serializer.validated_data['confirmation_code']
            ):
                token = str(AccessToken.for_user(user))
                user_data = {'username': user.username, 'token': token}
                return Response(user_data, status=status.HTTP_200_OK)
            return Response(
                'Указан неверный код подтверждения',
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        AuthorAdminModeratorPermission,
        IsAuthenticatedOrReadOnly,
    ]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        AuthorAdminModeratorPermission,
        IsAuthenticatedOrReadOnly,
    ]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
