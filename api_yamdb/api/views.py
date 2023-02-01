from django.conf import settings
from django import views
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import filters, viewsets, status, views

from reviews.models import Review, Title, Category, Genre, Title

from .permissions import (
    AdminOrReadOnly,
    AuthorAdminModeratorPermission,
    IsAdmin,
    IsSuperUser,
)
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitlePostSerializer,
    CommentSerializer,
    ReviewSerializer,
    UserSignUpSerializer,
    UserSerializer,
    UserIsMeSerializer,
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
    permission_classes = [
        AdminOrReadOnly,
    ]


class GenreViewSet(CreateReadDeleteModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = [
        AdminOrReadOnly,
    ]


class TitleViewSet(CreateReadUpdateDeleteModelViewset):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')
    permission_classes = [
        AdminOrReadOnly,
    ]

    def get_serializer_class(self):
        if self.action in ('create', 'patch'):
            return TitlePostSerializer
        return TitleSerializer


class SignUpView(views.APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        try:
            user, _ = User.objects.get_or_create(
                username=username, email=email
            )
        except IntegrityError:
            return Response(
                'Это имя или email уже занято', status.HTTP_400_BAD_REQUEST
            )
        user.confirmation_code = default_token_generator.make_token(user)
        user.save()
        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код: {user.confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return Response(serializer.validated_data, status.HTTP_200_OK)


class TokenView(views.APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != confirmation_code:
            return Response(
                {
                    "confirmation_code": (
                        "Неверный код доступа " f"{confirmation_code}"
                    )
                },
                status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"token": str(RefreshToken.for_user(user).access_token)}
        )


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
        if serializer.is_valid():
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


class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAdmin | IsSuperUser,
    ]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = [
        filters.SearchFilter,
    ]
    search_fields = ('=username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['PATCH', 'GET'],
        detail=False,
        permission_classes=[
            IsAuthenticated,
        ],
        url_path='me',
        url_name='me',
    )
    def me(self, request):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                instance, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=self.request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)
