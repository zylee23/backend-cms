"""Custom Permission for diagnosis API."""

from rest_framework.permissions import BasePermission
from users.models import User


class IsDoctorOrAdmin(BasePermission):
    """Grant permission if auth user is either doctor or admin."""

    def has_permission(self, request, view):
        auth_user = request.user
        if auth_user.role != User.Role.PATIENT:
            return True
        return False
