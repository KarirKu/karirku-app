from rest_framework import permissions
from .models import Alumni, Mahasiswa

class IsCurrentUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user

class IsAlumniOrMahasiswaUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if isinstance(request.user, Alumni) or isinstance(request.user, Mahasiswa):
            return True
        return False