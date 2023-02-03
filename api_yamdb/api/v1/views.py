from django.core.exceptions import BadRequest
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly
)
from reviews.models import Category, Genre, Review, Title

from .custom_viewsets import (
    CreateReadDeleteModelViewSet,
    CreateReadUpdateDeleteModelViewset
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitlePostSerializer,
    TitleSerializer,
)
from .filters import TitleFilter
from .permissions import (
    AdminOrReadOnly,
    AuthorAdminModeratorPermission,
)


class CategoryViewSet(CreateReadDeleteModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)


class GenreViewSet(CreateReadDeleteModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)


class TitleViewSet(CreateReadUpdateDeleteModelViewset):
    http_method_names = (
        "get",
        "post",
        "patch",
        "delete",
    )
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (AdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitlePostSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        AuthorAdminModeratorPermission,
        IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        user = self.request.user
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        if Review.objects.filter(title=title).filter(author=user).exists():
            raise BadRequest('Второй раз отзыв отправлять нельзя!')
        serializer.save(author=user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        AuthorAdminModeratorPermission,
        IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
