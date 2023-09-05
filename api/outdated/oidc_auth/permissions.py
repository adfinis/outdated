from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    def has_permission(self, request, _):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, _):
        return self.has_permission(request, view)
