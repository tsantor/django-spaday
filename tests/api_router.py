from django.urls import include, path

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenVerifyView,
# )

# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()

app_name = "api"

# urlpatterns = router.urls
urlpatterns = [
    # Place all your app's API URLS here.
    path("", include("django_spaday.api.urls")),
    # Auth (https://www.django-rest-framework.org/api-guide/authentication/)
    # path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("auth/", include("dj_rest_auth.urls")),
    # path("auth/registration/", include("dj_rest_auth.registration.urls")),
]
