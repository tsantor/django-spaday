import pytest

from django_spaday.api.serializers import UserAuthSerializer


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
