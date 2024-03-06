from auditlog.models import LogEntry
from dj_rest_auth.views import LoginView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission, update_last_login
from django_celery_results.models import TaskResult
from django_filters.rest_framework import DjangoFilterBackend
from django_perm_filter import filter_perms
from drf_spectacular.utils import extend_schema
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ..settings import api_settings
from ..utils import permissions_as_combobox
from .pagination import StandardPagination
from .serializers import (
    GroupAddUserSerializer,
    GroupRemoveUserSerializer,
    LogEntrySerializer,
    PermissionSerializer,
    TaskResultSerializer,
)
from .serializers.filters import LogEntryFilter
from .viewsets import MyModelViewSet

# from rest_framework.generics import GenericAPIView
# from django.middleware.csrf import get_token
# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page

User = get_user_model()


# class CsrfTokenView(GenericAPIView):
#     """CSRF Token"""

#     http_method_names = ["get"]
#     serializer_class = CsrfSerializer

#     def get(self, request):
#         serializer = self.get_serializer(data={"csrfToken": get_token(request)})
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data)


@extend_schema(tags=["spaday"])
class MyLoginView(LoginView):
    """Override dj_rest_auth LoginView so we can update last_login."""

    def login(self):
        super().login()
        update_last_login(None, self.user)


@extend_schema(tags=["spaday"])
class UserViewSet(MyModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = User.objects.all().order_by("last_name")
    permission_classes = (IsAuthenticated,)  # DjangoModelPermissions
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["first_name", "last_name", "email"]
    ordering_fields = [
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_superuser",
        "last_login",
    ]

    def get_serializer_class(self):
        actions = {
            "change_password": api_settings.CHANGE_PASSWORD_SERIALIZER,
            "recent_logins": api_settings.LAST_LOGIN_SERIALIZER,
        }
        return actions.get(self.action, api_settings.USER_SERIALIZER)

    @action(detail=True, methods=["put"], url_path=r"password")
    def change_password(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()

    @action(detail=False, methods=["get"], url_path=r"recent-logins")
    def recent_logins(self, request):
        if request.user.is_superuser:
            recent_users = User.objects.exclude(
                last_login__isnull=True,
                is_staff=False,
            ).order_by(
                "-last_login"
            )[:10]
        else:
            # TODO: Clean this up as not all users have a company
            if hasattr(request.user, "company"):
                recent_users = (
                    User.objects.filter(company=request.user.company)
                    .exclude(last_login__isnull=True, is_staff=False)
                    .order_by("-last_login")[:10]
                )
            else:
                recent_users = User.objects.filter(pk=request.user.pk, is_staff=True)
        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)


@extend_schema(tags=["spaday"])
class GroupViewSet(MyModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Group.objects.all().order_by("name")
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]

    def get_serializer_class(self):
        actions = {
            "users": api_settings.USER_SERIALIZER,
            "add_users": GroupAddUserSerializer,
            "remove_users": GroupRemoveUserSerializer,
        }
        return actions.get(self.action, api_settings.GROUP_SERIALIZER)

    @action(detail=True, methods=["get"])
    def users(self, request, pk=None):
        """Return all users in this Group."""
        obj = self.get_object()
        serializer = self.get_serializer(
            obj.user_set.all().order_by("last_name", "first_name"),
            many=True,
        )
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path=r"add-users")
    def add_users(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path=r"remove-users")
    def remove_users(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False)
    def combobox(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


@extend_schema(tags=["spaday"])
class PermissionViewSet(GenericViewSet):
    queryset = filter_perms(Permission.objects.all())
    serializer_class = PermissionSerializer
    permission_classes = (IsAuthenticated,)

    # @method_decorator(cache_page(60 * 60 * 2))
    @action(detail=False)
    def combobox(self, request, *args, **kwargs):
        return Response(permissions_as_combobox(self.get_queryset()))


@extend_schema(tags=["spaday"])
class LogEntryViewSet(MyModelViewSet):
    """Integration with django-auditlog."""

    http_method_names = ["get", "delete"]
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = [
        "content_type__model",
        "object_repr",
        "actor__first_name",
        "actor__last_name",
        "actor__email",
        "remote_addr",
    ]
    filterset_class = LogEntryFilter


@extend_schema(tags=["spaday"])
class TaskResultViewSet(MyModelViewSet):
    """Integration with django-celery-results."""

    http_method_names = ["get", "delete"]
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "periodic_task_name",
        "task_name",
        "task_args",
        "task_kwargs",
    ]
    ordering_fields = [
        "periodic_task_name",
        "task_name",
        "status",
        "date_done",
        "worker",
    ]
