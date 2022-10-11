"""Custom permissions."""

from rest_framework import permissions


class IsAdminRoleOrSuperUser(permissions.BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == "admin" or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.role == "admin" or request.user.is_superuser
        )
