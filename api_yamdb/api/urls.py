from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SignUpView, TokenView

router = DefaultRouter()
#router.register('users', UsersViewSet, basename='users')


auth_patterns = [
    path('signup/', SignUpView.as_view()),
    path('token/', TokenView.as_view())
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth_patterns)),
]

