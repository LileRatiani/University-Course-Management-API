from rest_framework import permissions

class IsProfessorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow professors to edit an object.
    Students can only view (GET requests).
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to professors.
        return request.user.is_authenticated and request.user.role == 'professor'