from auditlog.registry import auditlog
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models

User = get_user_model()

class GenericPerms(models.Model):
    class Meta:
        # No database table for this model
        managed = False

        # disable "add", "change", "delete" and "view" default permissions
        default_permissions = ()

        permissions = (("view_dashboard", "Can view dashboard"),)

auditlog.register(User, exclude_fields=['last_login', 'password'])
auditlog.register(Group)
