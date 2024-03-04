import pytest
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from .factories import GroupFactory, LogEntryFactory, TaskResultFactory


@pytest.fixture
def content_type():
    return ContentType.objects.create(app_label="test_app", model="test_model")


@pytest.fixture
def permission(content_type):
    return Permission.objects.create(
        codename="test_permission",
        name="Test Permission",
        content_type=content_type,
    )


@pytest.fixture
def group():
    return GroupFactory.create()


# @pytest.fixture
# def user(group):
#     return UserFactory.create(groups=[group]


@pytest.fixture
def log_entry(user):
    return LogEntryFactory.create(actor=user)


@pytest.fixture
def task_result():
    return TaskResultFactory.create()
