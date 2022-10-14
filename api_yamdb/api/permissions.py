from rest_framework import permissions
from reviews.models import User

class IsAdmin(permissions.BasePermission):
    '''Пользовтель является админом,
и он авторизирован.'''
    def has_permission(self, request, obj):
        return (
            request.user.role == User.is_authenticated
            and request.user.role == User.is_admin
        )

class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.is_moderator


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.pk == request.user.pk


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
        or request.user.role == User.is_admin
        or request.user.role == User.is_moderator
        or obj.author == request.user)