from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'moderator'


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.pk == request.user.pk


# class IsAuthorOrReadOnly(permissions.BasePermission):

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj.author == request.user


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
        or request.user.role == 'admin'
        or request.user.role == 'moderator'
        or obj.author == 'user')
