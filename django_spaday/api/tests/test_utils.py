import pytest

from django_spaday.tests.factories import UserFactory

from ..utils import get_deleted_objects


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
