import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

import factories

User = get_user_model()


@pytest.fixture
def user():
    return factories.UserFactory()


@pytest.fixture
def superuser():
    return factories.UserFactory(is_superuser=True, is_staff=True)


# @pytest.fixture(scope="session")
# def django_db_setup(django_db_setup, django_db_blocker):
#     with django_db_blocker.unblock():
#         # Use our fixtures
#         call_command("loaddata", "dump.json")


@pytest.fixture
def test_user():
    return User.objects.create_user(username="testuser@test.com", password="testpass")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, test_user):
    """Authenticate the API client with the test user."""
    api_client.login(username=test_user.username, password="testpass")
    return api_client


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath
