from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SignUpView, TokenView, CommentViewSet, ReviewViewSet


v1_router = DefaultRouter()
# router.register('users', UsersViewSet, basename='users')

v1_router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                   basename='reviews')

v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

app_name = 'api'

auth_patterns = [
    path('signup/', SignUpView.as_view()),
    path('token/', TokenView.as_view())
]

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/', include(auth_patterns)),
]
