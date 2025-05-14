from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if user.role == 'admin':
            return True

        if user.role == 'agent' and obj.owner == user:
            return True

        return False


class IsAgentOrAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and getattr(user, 'role', None) in ['agent', 'admin']
