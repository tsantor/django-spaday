from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SpaDayConfig(AppConfig):
    name = "django_spaday"
    verbose_name = _("SPA Day")
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        pass
