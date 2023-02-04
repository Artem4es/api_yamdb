from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminOrReadOnly(BasePermission):
    """
    Для использования т.к. безопасных методов, пользователь должен быть
    авторизован и обладать админскими привелегиями в приложении.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class AuthorAdminModeratorPermission(BasePermission):
    """
    Для использования безопасных методов пользователь должен быть
    авторизован и обладать одним из следующих уровеней доступа
    - суперадмин
    - админ
    - модератор
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_superuser
            or request.user.is_admin
            or request.user.is_moderator
        )


class IsSuperUser(BasePermission):
    """
    Права доступа пользователя должны быть суперадмин.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class IsAdmin(BasePermission):
    """
    Права доступа пользователя должны быть админскими.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_admin)
