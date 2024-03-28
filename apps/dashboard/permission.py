from rest_framework.permissions import BasePermission

from apps.dashboard.models import Ticket


class IsOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        return obj.user == request.user