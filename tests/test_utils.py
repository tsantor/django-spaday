import pytest
from django.contrib.auth.models import Permission

from django_spaday.api.utils import get_deleted_objects
from django_spaday.utils import permissions_as_combobox
from tests.factories import UserFactory


@pytest.mark.django_db
def test_permissions_as_combobox(permission):
    permissions = Permission.objects.filter(pk=permission.id)
    result = permissions_as_combobox(permissions)
    expected_result = [
        {"header": "Test_App"},
        {"divider": True},
        {"value": permission.id, "text": "Test Permission"},
    ]
    assert result == expected_result


@pytest.mark.django_db
def test_get_deleted_objects():
    # Create a User instance to test with
    user = UserFactory.create()

    # Call the function with the User instance
    to_delete, model_count, protected = get_deleted_objects([user])

    # Check that the function returns the correct results
    assert to_delete == [f"User: {user}"]
    assert model_count == {"users": 1}
    assert protected == []
