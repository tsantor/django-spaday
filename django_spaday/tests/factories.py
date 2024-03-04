import factory
from auditlog.models import LogEntry
from celery import states
from django.contrib.admin.models import ADDITION
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType
from django_celery_results.models import TaskResult

User = get_user_model()


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Sequence(lambda n: f"group{n}")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "defaultpassword")


class LogEntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LogEntry

    content_type = factory.LazyAttribute(lambda _: ContentType.objects.get_for_model(LogEntry))
    # content_type = factory.SubFactory(ContentTypeFactory)
    object_pk = factory.Faker("pyint")
    object_repr = factory.Faker("word")

    action = LogEntry.Action.CREATE

    # changes = {"name": ["Old", "New"]}
    changes = None
    actor = factory.SubFactory(UserFactory)


class TaskResultFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TaskResult

    task_id = factory.Faker("uuid4")
    task_name = factory.Faker("word")
    task_args = "[]"
    task_kwargs = "{}"
    status = states.SUCCESS
    result = factory.Faker("word")
    traceback = None
    worker = factory.Faker("word")