from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if request.user.role == 'agent' and obj.owner == request.user:
            return True
        return False