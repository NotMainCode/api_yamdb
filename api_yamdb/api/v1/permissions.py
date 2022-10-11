"""Custom permissions."""

from rest_framework import permissions


class IsAdminUserOrSuperUser(permissions.BasePermission):
    """Permission to act only to user with "admin" role."""

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser
        )
