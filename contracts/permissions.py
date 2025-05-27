from rest_framework.permissions import BasePermission

class IsAgentOrAdminContract(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['agent', 'admin']

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj.agent == request.user