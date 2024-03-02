# -*- coding: utf-8 -*-

from rest_framework.permissions import IsAdminUser  # BasePermission


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return request.user.is_superuser


# class IsAuthenticated(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_active
