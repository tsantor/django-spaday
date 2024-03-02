from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# -----------------------------------------------------------------------------

# Routers provide an easy way of automatically determining the URL conf.
router = DefaultRouter()
router.register(r"users", views.UserViewSet, basename="users")
router.register(r"groups", views.GroupViewSet, basename="groups")
router.register(r"permissions", views.PermissionViewSet, basename="permissions")

router.register(r"auditlogs", views.LogEntryViewSet, basename="auditlogs")
router.register(r"taskresults", views.TaskResultViewSet, basename="taskresults")


urlpatterns = [
    path("", include(router.urls)),
    # path("csrf/", views.CsrfTokenView.as_view()),
    # Override dj_rest_auth LoginView
    # path("auth/login/", views.MyLoginView.as_view()),
]
