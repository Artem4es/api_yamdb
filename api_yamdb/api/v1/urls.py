from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import SignUpView, TokenView, UsersViewSet
from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
)

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register(r'users', UsersViewSet, basename='users')
v1_router.register(r'categories', CategoryViewSet)
v1_router.register(r'genres', GenreViewSet)
v1_router.register(r'titles', TitleViewSet)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

auth_patterns = [
    path('signup/', SignUpView.as_view()),
    path('token/', TokenView.as_view()),
]

urlpatterns = [
    path('auth/', include(auth_patterns)),
    path('', include(v1_router.urls)),
]
