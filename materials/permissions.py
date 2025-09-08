from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Разрешение: пользователь является модератором"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name="moderators").exists()
        )
