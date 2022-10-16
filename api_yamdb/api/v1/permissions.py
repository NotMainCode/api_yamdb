"""Custom permissions."""

from rest_framework import permissions


def admin_role(request):
    return request.user.is_authenticated and request.user.is_admin


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """Full access: admin, moderator, content author. Reading: other users."""

    message = "You do not have permission to perform this action."

    def has_object_permission(self, request, view, obj):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user == obj.author
                or request.user.is_moderator
                or admin_role(request)
        )

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS) or (
            request.user.is_authenticated)


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Full access: content author. Reading: other users."""

    message = "Only author has permission to perform this action."

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS) or (
            request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS) or (
                obj.author == request.user)


class IsAdminRoleOrReadOnly(permissions.BasePermission):
    """Full access: admin. Reading: other users."""

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        return ((request.method in permissions.SAFE_METHODS) or (
            admin_role(request)))


class IsAdminRole(permissions.BasePermission):
    """Only administrator."""

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        return admin_role(request)
