"""Custom permissions."""

from rest_framework import permissions


def safe_methods(request):
    return request.method in permissions.SAFE_METHODS


def safe_methods_or_authenticated(request):
    return safe_methods(request) or request.user.is_authenticated


def safe_methods_or_admin_moderator(request):
    return safe_methods(request) or (
        request.user.is_authenticated
        and (request.user.is_admin or request.user.is_moderator)
    )


def admin_role_or_superuser(request):
    return request.user.is_authenticated and (
        request.user.is_admin or request.user.is_superuser
    )


def admin_role(request):
    return request.user.is_authenticated and request.user.is_admin


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """Full access: admin, moderator, content author. Reading: other users."""

    message = "You do not have permission to perform this action."

    def has_object_permission(self, request, view, obj):
        return (
            safe_methods_or_admin_moderator(request)
            or obj.author == request.user
        )

    def has_permission(self, request, view):
        return safe_methods_or_authenticated(request)


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Full access: content author. Reading: other users."""

    message = "Only author has permission to perform this action."

    def has_permission(self, request, view):
        return safe_methods_or_authenticated(request)

    def has_object_permission(self, request, view, obj):
        return safe_methods(request) or obj.author == request.user


class IsAdminRoleOrReadOnly(permissions.BasePermission):
    """Full access: admin. Reading: other users."""

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        return safe_methods(request) or admin_role(request)

    def has_object_permission(self, request, view, obj):
        return safe_methods_or_admin_moderator(request)


class IsAdminRoleOrSuperUser(permissions.BasePermission):
    """Only administrator and superuser access."""

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        return admin_role_or_superuser(request)
