from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


# class CsrfSerializer(serializers.Serializer):
#     csrfToken = serializers.CharField()


class PermissionSerializer(serializers.ModelSerializer):
    """Serializer for v-combobox. This can be overriden in the SPA_DAY settings."""

    value = serializers.IntegerField(source="pk")
    text = serializers.CharField(source="name")

    class Meta:
        model = Permission
        fields = ["value", "text"]


class GroupAddUserSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        source="user_set",
    )

    class Meta:
        model = Group
        fields = ["users"]

    def update(self, instance, validated_data):
        users = validated_data.pop("user_set", [])
        instance.user_set.add(*users)
        return instance


class GroupRemoveUserSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        source="user_set",
    )

    class Meta:
        model = Group
        fields = ["users"]

    def update(self, instance, validated_data):
        users = validated_data.pop("user_set", [])
        instance.user_set.remove(*users)
        return instance


class GroupSerializer(serializers.ModelSerializer):
    """This can be overriden in the SPA_DAY settings."""

    num_users = serializers.SerializerMethodField()

    # users = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=User.objects.all(), source="user_set"
    # )

    class Meta:
        model = Group
        fields = ["pk", "name", "permissions", "num_users"]

    # def create(self, validated_data):
    #     """Handle our nested Permissions"""
    #     permissions = validated_data.pop("permissions", [])
    #     group = super().create(validated_data)
    #     group.permissions.set(list(permissions))
    #     return group

    # def update(self, instance, validated_data):
    #     permissions = validated_data.pop("permissions", [])
    #     group = super().update(instance, validated_data)
    #     group.permissions.set(list(permissions))
    #     return group

    def get_num_users(self, instance) -> int:
        return instance.user_set.all().count()


class UserSerializer(serializers.ModelSerializer):
    """This can be overriden in the SPA_DAY settings."""

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
        return ""

    def get_full_name(self, instance) -> str:
        if instance.first_name and instance.last_name:
            return f"{instance.first_name} {instance.last_name}"
        return ""

    def create(self, validated_data):
        validated_data["email"] = validated_data["email"].lower()
        if "username" in User._meta.get_fields():
            validated_data["username"] = validated_data["email"]
        password = validated_data.pop("password")
        # groups = validated_data.pop("groups")
        # permissions = validated_data.pop("user_permissions")

        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        # user.groups.set(list(groups))
        # user.user_permissions.set(list(permissions))
        return user

    def update(self, instance, validated_data):
        # This ensures the username is email, and email is lower case
        if "email" in validated_data:
            validated_data["email"] = validated_data["email"].lower()

        if "username" in User._meta.get_fields():
            validated_data["username"] = validated_data.pop("email", None)

        # groups = validated_data.pop("groups")
        # permissions = validated_data.pop("user_permissions")

        user = super().update(instance, validated_data)
        # user.save()

        # user.groups.set(list(groups))
        # user.user_permissions.set(list(permissions))
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    """This can be overriden in the SPA_DAY settings."""

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    # old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    # def create(self, validated_data):
    #     print("Do not call me")

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


class UserAuthSerializer(serializers.ModelSerializer):
    """This can be overriden in the SPA_DAY settings."""

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
        return sorted(list(instance.get_all_permissions()))

    def get_initials(self, instance) -> str:
        if instance.first_name and instance.last_name:
            first_name = instance.first_name[0]
            last_name = instance.last_name[0]
            return f"{first_name}{last_name}".upper()

    def get_full_name(self, instance) -> str:
        if instance.first_name and instance.last_name:
            return f"{instance.first_name} {instance.last_name}"


class LastLoginSerializer(serializers.ModelSerializer):
    """This can be overriden in the SPA_DAY settings."""

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
