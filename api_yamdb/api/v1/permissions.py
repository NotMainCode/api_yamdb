"""Custom permissions."""

from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Object-level permission to only allow authors of object to edit it."""

    message = "Only the author has permission to perform this action."

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )

