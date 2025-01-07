from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # the safe methods from django permissions( SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS'))
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
