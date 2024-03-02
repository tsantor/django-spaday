import pytest
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


@pytest.fixture
def content_type():
    return ContentType.objects.create(app_label="test_app", model="test_model")


@pytest.fixture
def permission(content_type):
    return Permission.objects.create(
        codename="test_permission", name="Test Permission", content_type=content_type
    )
