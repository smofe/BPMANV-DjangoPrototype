from rest_framework import permissions


class IsAdminOrAuthenticatedReadOnly(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        is_admin = request.user.is_staff
        is_read_only = request.method in permissions.SAFE_METHODS
        return (is_authenticated and is_read_only) or is_admin

