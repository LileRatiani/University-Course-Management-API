from rest_framework import permissions

class IsSelfOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow users to view/edit their own profile,
    unless they are an admin.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.role == 'admin'