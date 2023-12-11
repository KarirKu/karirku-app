from rest_framework import permissions
from user.models import User

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            return obj.alumni == User.objects.get(id=request.user.id)
        except:
            return False
