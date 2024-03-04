import json

from auditlog.models import LogEntry
from django.apps import apps
from rest_framework import serializers


class LogEntrySerializer(serializers.ModelSerializer):
    """django-auditlog integration."""

    app = serializers.SerializerMethodField()
    model = serializers.SerializerMethodField()
    action = serializers.SerializerMethodField()
    changes = serializers.SerializerMethodField()
    changes_summary = serializers.SerializerMethodField()
    user = serializers.StringRelatedField(source="actor")

    class Meta:
        model = LogEntry
        fields = (
            "pk",
            "content_type",
            "app",
            "model",
            "object_repr",
            "action",
            "changes",
            "changes_summary",
            "user",
            "remote_addr",
            "timestamp",
        )

    def get_app(self, obj) -> str:
        """Return a Title Case model name."""
        app = apps.get_app_config(obj.content_type.app_label)
        return app.verbose_name.title()

    def get_model(self, obj) -> str:
        """Return a Title Case model name."""
        model = apps.get_model(obj.content_type.app_label, obj.content_type.model)
        return model._meta.verbose_name.title()

    def get_changes(self, obj) -> dict:
        """Compatible with v-datatable."""
        return [
            {
                "#": i + 1,
                "field": k,
                "from": v[0],
                "to": v[1],
            }
            for i, (k, v) in enumerate(obj.changes_dict.items())
        ]

    def get_action(self, obj) -> str:
        actions = {
            "0": "Create",
            "1": "Update",
            "2": "Delete",
            "3": "Access",
        }
        if str(obj.action) in actions:
            return actions.get(str(obj.action))

    def get_changes_summary(self, obj) -> str:
        """Extracted from auditlog/mixins.py"""
        MAX = 75
        if obj.action == LogEntry.Action.DELETE:
            return ""  # delete
        changes = json.loads(obj.changes)
        s = "" if len(changes) == 1 else "s"
        fields = ", ".join(changes.keys())
        if len(fields) > MAX:
            i = fields.rfind(" ", 0, MAX)
            fields = f"{fields[:i]} .."
        return f"{len(changes)} change{s}: {fields}"
