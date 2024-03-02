import json

from auditlog.models import LogEntry
from django.apps import apps
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from django_celery_results.models import TaskResult

User = get_user_model()


class CsrfSerializer(serializers.Serializer):

    csrfToken = serializers.CharField()


class PermissionListSerializer(serializers.ModelSerializer):
    """Serializer for v-combobox."""

    value = serializers.IntegerField(source="pk")
    text = serializers.CharField(source="name")

    class Meta:
        model = Permission
        fields = ["value", "text"]
        extra_kwargs = {
            "value": {"read_only": True},
            "text": {"read_only": True},
        }


class GroupAddUserSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), source="user_set"
    )

    class Meta:
        model = Group
        fields = ["users"]

    def update(self, instance, validated_data):
        users = validated_data.pop("user_set", [])
        # instance = super().update(instance, validated_data)
        for u in users:
            instance.user_set.add(u)
        return instance


class GroupRemoveUserSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), source="user_set"
    )

    class Meta:
        model = Group
        fields = ["users"]

    def update(self, instance, validated_data):
        users = validated_data.pop("user_set", [])
        # instance = super().update(instance, validated_data)
        for u in users:
            instance.user_set.remove(u)
        return instance


class GroupSerializer(serializers.ModelSerializer):
    num_users = serializers.SerializerMethodField()

    # users = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=User.objects.all(), source="user_set"
    # )

    class Meta:
        model = Group
        fields = ["pk", "name", "permissions", "num_users"]

    def create(self, validated_data):
        """Handle our nested Permissions"""
        permissions = validated_data.pop("permissions")
        group = super().create(validated_data)
        group.permissions.set(list(permissions))
        return group

    def update(self, instance, validated_data):
        permissions = validated_data.pop("permissions")
        group = super().update(instance, validated_data)
        group.permissions.set(list(permissions))
        return group

    def get_num_users(self, instance) -> int:
        return instance.user_set.all().count()


class UserSerializer(serializers.ModelSerializer):

    initials = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "pk",
            "is_active",
            "is_superuser",
            "is_staff",
            "first_name",
            "last_name",
            "email",
            "last_login",
            "groups",
            "user_permissions",
            "password",
            "initials",
            "full_name",
        )

        extra_kwargs = {
            "pk": {"read_only": True},
            "last_login": {"read_only": True},
            "password": {
                "write_only": True,
                "required": False,
            },
        }

    def get_initials(self, instance) -> str:
        if instance.first_name and instance.last_name:
            first_name = instance.first_name[0]
            last_name = instance.last_name[0]
            return f"{first_name}{last_name}".upper()

    def get_full_name(self, instance) -> str:
        if instance.first_name and instance.last_name:
            return f"{instance.first_name} {instance.last_name}"

    def create(self, validated_data):
        validated_data["username"] = validated_data["email"]
        password = validated_data.pop("password")
        groups = validated_data.pop("groups")
        permissions = validated_data.pop("user_permissions")

        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        user.groups.set(list(groups))
        user.user_permissions.set(list(permissions))
        return user

    def update(self, instance, validated_data):
        validated_data["username"] = validated_data["email"]
        groups = validated_data.pop("groups")
        permissions = validated_data.pop("user_permissions")

        user = super().update(instance, validated_data)
        user.save()

        user.groups.set(list(groups))
        user.user_permissions.set(list(permissions))
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    # old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value

    def create(self, validated_data):
        print("Do not call me")

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


class UserAuthSerializer(serializers.ModelSerializer):
    """Serializer for User Auth only."""

    initials = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    permissions_codenames = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "pk",
            "is_active",
            "is_superuser",
            "is_staff",
            "first_name",
            "last_name",
            "email",
            "permissions_codenames",
            "initials",
            "full_name",
        )

    def get_permissions_codenames(self, instance) -> list:
        return instance.get_all_permissions()

    def get_initials(self, instance) -> str:
        if instance.first_name and instance.last_name:
            first_name = instance.first_name[0]
            last_name = instance.last_name[0]
            return f"{first_name}{last_name}".upper()

    def get_full_name(self, instance) -> str:
        if instance.first_name and instance.last_name:
            return f"{instance.first_name} {instance.last_name}"


class LastLoginSerializer(serializers.ModelSerializer):
    """Serializer for v-datatable."""

    class Meta:
        model = User
        fields = (
            "pk",
            "first_name",
            "last_name",
            "email",
            "is_superuser",
            "is_staff",
            "last_login",
        )


class LogEntrySerializer(serializers.ModelSerializer):
    """For django-auditlog integration."""

    # label = serializers.SerializerMethodField()
    model = serializers.SerializerMethodField()
    action = serializers.SerializerMethodField()
    changes = serializers.SerializerMethodField()
    changes_summary = serializers.SerializerMethodField()
    user = serializers.StringRelatedField(source="actor")

    class Meta:
        model = LogEntry
        fields = (
            "pk",
            # "label",
            "model",
            # "object_pk",
            # "object_id",
            "object_repr",
            "action",
            "changes",
            "changes_summary",
            "user",
            "remote_addr",
            "timestamp",
            # "additional_data",
        )

        extra_kwargs = {
            "pk": {"read_only": True},
            "timestamp": {"read_only": True},
        }

    # def get_label(self, obj) -> str:
    #     return obj.__str__()

    def get_model(self, obj) -> str:
        """Return a Title Case model name."""
        model = apps.get_model(obj.content_type.app_label, obj.content_type.model)
        return model._meta.verbose_name.title()

    def get_changes(self, obj) -> dict:
        """Compatible with v-datatable."""
        return [
            {
                "#": i + 1,
                "field": k,
                "from": v[0],
                "to": v[1],
            }
            for i, (k, v) in enumerate(obj.changes_dict.items())
        ]

    def get_action(self, obj) -> str:
        actions = {
            "0": "Create",
            "1": "Update",
            "2": "Delete",
        }
        if str(obj.action) in actions:
            return actions.get(str(obj.action))

    def get_changes_summary(self, obj) -> str:
        """Extracted from auditlog/mixins.py"""
        MAX = 75
        if obj.action == LogEntry.Action.DELETE:
            return ""  # delete
        changes = json.loads(obj.changes)
        s = "" if len(changes) == 1 else "s"
        fields = ", ".join(changes.keys())
        if len(fields) > MAX:
            i = fields.rfind(" ", 0, MAX)
            fields = f"{fields[:i]} .."
        return f"{len(changes)} change{s}: {fields}"


class TaskResultSerializer(serializers.ModelSerializer):
    """For django-celery-results integration."""

    class Meta:
        model = TaskResult
        fields = [
            "pk",
            "task_id",
            "periodic_task_name",
            "task_name",
            "task_args",
            "task_kwargs",
            "status",
            "worker",
            "content_type",
            "content_encoding",
            "result",
            "date_created",
            "date_done",
            "traceback",
            "meta",
        ]
