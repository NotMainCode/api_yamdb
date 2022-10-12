"""Custom permissions."""

from rest_framework import permissions


def safe_methods(request):
    return request.method in permissions.SAFE_METHODS


def safe_methods_or_authenticated(request):
    return safe_methods(request) or request.user.is_authenticated


def safe_methods_or_admin_moderator(request):
    return safe_methods(request) or (
        request.user.is_authenticated
        and (request.user.role in ["admin", "moderator"])
    )


def admin_role_or_superuser(request):
    return request.user.is_authenticated and (
        request.user.role == "admin" or request.user.is_superuser
    )


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    message = "You do not have permission to perform this action."

    def has_object_permission(self, request, view, obj):
        return (
            safe_methods_or_admin_moderator(request)
            or obj.author == request.user
        )

    def has_permission(self, request, view):
        return safe_methods_or_authenticated(request)


class IsAuthorOrReadOnly(permissions.BasePermission):
    message = "Only the author has permission to perform this action."

    def has_permission(self, request, view):
        return safe_methods_or_authenticated(request)

    def has_object_permission(self, request, view, obj):
        return safe_methods(request) or obj.author == request.user


class IsAdminRoleSuperUserOrReadOnly(permissions.BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        return safe_methods(request) or (admin_role_or_superuser(request))

    def has_object_permission(self, request, view, obj):
        return safe_methods_or_admin_moderator(request)


class IsAdminRoleOrSuperUser(permissions.BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        return admin_role_or_superuser(request)

    def has_object_permission(self, request, view, obj):
        return admin_role_or_superuser(request)
