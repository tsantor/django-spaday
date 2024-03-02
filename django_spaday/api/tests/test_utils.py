import pytest
from django.contrib.auth import get_user_model

from ..utils import get_deleted_objects


@pytest.mark.django_db
def test_get_deleted_objects():
    # Create a User instance to test with
    user = get_user_model().objects.create_user(username="testuser", password="12345")

    # Call the function with the User instance
    to_delete, model_count, protected = get_deleted_objects([user])

    # Check that the function returns the correct results
    assert to_delete == [f"User: {user}"]
    assert model_count == {"users": 1}
    assert protected == []
