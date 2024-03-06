import django_filters
from auditlog.models import LogEntry


class LogEntryFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(
        fields=(
            ("content_type__app_label", "app"),
            ("content_type__model", "model"),
            ("object_repr"),
            ("action"),
            ("actor", "user"),
            ("remote_addr"),
            ("timestamp"),
        )
    )

    class Meta:
        model = LogEntry
        fields = [
            "content_type",
            "object_repr",
            "action",
            "actor",
            "remote_addr",
            "timestamp",
        ]
