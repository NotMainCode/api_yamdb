"""Custom permissions."""

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminModeratorAuthorOrReadOnly(BasePermission):
    """Full access: admin, moderator, content author. Reading: other users."""

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user == obj.author
            or request.user.is_moderator
            or request.user.is_admin
        )


class IsAdminOrReadOnly(BasePermission):
    """Full access: admin. Reading: other users."""

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAdmin(BasePermission):
    """Only administrator."""

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
