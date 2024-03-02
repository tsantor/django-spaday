import pytest
from django.contrib.auth.models import Permission

from ..utils import permissions_as_combobox


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
