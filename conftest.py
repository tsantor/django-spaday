import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

import factories

User = get_user_model()

# @pytest.fixture(scope="session")
# def django_db_setup(django_db_setup, django_db_blocker):
#     with django_db_blocker.unblock():
#         # Use our fixtures
#         call_command("loaddata", "dump.json")


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user():
    return User.objects.create_user(
        username="user@test.com",
        email="user@test.com",
        password="testpass",
    )


@pytest.fixture
def staff():
    return User.objects.create_user(
        username="staff@test.com",
        email="staff@test.com",
        password="testpass",
        is_staff=True,
    )


@pytest.fixture
def superuser():
    return factories.UserFactory(
        username="superuser@test.com",
        email="superuser@test.com",
        password="testpass",
        is_superuser=True,
        is_staff=True,
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    """Authenticate the API client with the test user."""
    api_client.login(username=user.username, password="testpass")
    return api_client


@pytest.fixture
def staff_authenticated_client(api_client, staff):
    """Authenticate the API client with the test user."""
    api_client.login(username=staff.username, password="testpass")
    return api_client


@pytest.fixture
def superuser_authenticated_client(api_client, superuser):
    """Authenticate the API client with the test user."""
    api_client.login(username=superuser.username, password="testpass")
    return api_client
