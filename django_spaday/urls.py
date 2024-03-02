from django.urls import path
from django.views.generic.base import RedirectView

from .views import AdminView

app_name = "spaday"

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="spaday:admin")),
    path("admin/", view=AdminView.as_view(), name="admin"),
    path("admin/<path:catch_all>", view=AdminView.as_view(), name="admin"),
]
