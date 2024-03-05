import pytest

from django_spaday.api.serializers import ChangePasswordSerializer, UserAuthSerializer


@pytest.mark.django_db
def test_user_auth_serializer(user):
    serializer = UserAuthSerializer(user)
    data = serializer.data

    assert data["pk"] == user.pk
    assert data["is_active"] == user.is_active
    assert data["is_superuser"] == user.is_superuser
    assert data["is_staff"] == user.is_staff
    assert data["first_name"] == user.first_name
    assert data["last_name"] == user.last_name
    assert data["email"] == user.email
    assert data["permissions_codenames"] == sorted(list(user.get_all_permissions()))
    assert data["initials"] == "UU"
    assert data["full_name"] == "User User"


@pytest.mark.django_db
def test_change_password_serializer(user):
    data = {"password": "new_password", "password2": "new_password"}
    serializer = ChangePasswordSerializer(data=data, context={"request": user})
    assert serializer.is_valid()
    validated_data = serializer.validated_data
    assert validated_data["password"] == "new_password"
    assert validated_data["password2"] == "new_password"

    instance = serializer.update(user, validated_data)
    assert instance.check_password("new_password")


@pytest.mark.django_db
def test_change_password_serializer_non_matching(user):
    data = {"password": "new_password", "password2": "new_password2"}
    serializer = ChangePasswordSerializer(data=data, context={"request": user})
    assert serializer.is_valid() is False
    assert serializer.errors == {"password": ["Password fields didn't match."]}
