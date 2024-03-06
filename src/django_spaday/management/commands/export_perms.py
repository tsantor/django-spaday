from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "My shiny new management command."

    # def add_arguments(self, parser):
    #     parser.add_argument("file")
    #     parser.add_argument("project")

    def handle(self, *args, **options):
        perms = Permission.objects.all()

        ignore_apps = [
            "admin.logentry" "authtoken.tokenproxy",
            "contenttypes",
            "django_celery_beat",
            "django_celery_results",
            "sessions",
            "sites",
            "socialaccount",
        ]

        # with open("permissions.js", "w") as file:
        for p in perms:
            # const = p.name.upper().replace(" ", "_")
            codename = f"{p.content_type.app_label}.{p.codename}"

            if p.content_type.app_label in ignore_apps:
                continue

            # file.write(f"export const {const} = '{codename}'\n")
            print(codename)
