"""Custom permissions."""

from rest_framework import permissions


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            (request.method in permissions.SAFE_METHODS)
            or (
                request.user.is_authenticated
                and (request.user.role in ["admin", "moderator"])
            )
            or obj.author == request.user
        )

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )


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
        ) or obj.author == request.user


class IsAdminRoleSuperUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS) or (
            request.user.is_authenticated
            and (request.user.is_superuser or (request.user.role in ["admin"]))
        )

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS) or (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or (request.user.role in ["admin", "moderator"])
            )
        )


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
