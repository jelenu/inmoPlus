from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAgentOrAdminClient(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role in ['admin', 'agent']

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == 'admin':
            return True
        if user.role == 'agent' and obj.agent == user:
            return True
        return False