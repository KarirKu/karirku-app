from rest_framework import permissions
from user.models import Alumni

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            return obj.alumni == Alumni.objects.get(id=request.user.id)
        except:
            return False

class IsAlumniUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            Alumni.objects.get(id=request.user.id)
            return True
        except:
            return False