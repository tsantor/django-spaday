from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from . import api_router

admin.site.enable_nav_sidebar = False

# from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path(r"djadmin/", admin.site.urls),
    path("", include("django_spaday.urls")),
]

# API URLS
urlpatterns += [
    # API base url
    path("api/v1/", include(api_router)),
    # DRF auth token
    # path("auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="api-schema"), name="redoc"),
]
