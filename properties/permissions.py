from rest_framework.permissions import BasePermission

class IsAgentOrAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['agent', 'admin']