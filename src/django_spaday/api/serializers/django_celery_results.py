from django_celery_results.models import TaskResult
from rest_framework import serializers


class TaskResultSerializer(serializers.ModelSerializer):
    """django-celery-results integration."""

    class Meta:
        model = TaskResult
        fields = [
            "pk",
            "task_id",
            "periodic_task_name",
            "task_name",
            "task_args",
            "task_kwargs",
            "status",
            "worker",
            "content_type",
            "content_encoding",
            "result",
            "date_created",
            "date_done",
            "traceback",
            "meta",
        ]
