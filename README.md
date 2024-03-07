# Django SPA Day

A Django package that provides "out-of-the-box" basic auth, user, group, and permission APIs for use in Single Page Apps (eg - Vue, React).

So easy, you can take a SPA day!

`django-spaday` deliberately stays below version 1.x.x to signal that every new version may potentially have breaking changes.

> NOTE: `django-spaday` is _very_ opinionated as its for internal use.

## Features

- Auth (login/logout/change password)
- User management w/permissions
- Group management w/permissions
- Audit Log (optional)
- Django Celery Results (optional)

## Requirements

Assumes you have started from this [cookiecutter-django](https://github.com/tsantor/cookiecutter-django) template which leverages the following.

- dj-rest-auth
- django-auditlog
- django-celery-results
- django-cors-headers
- django-filter
- djangorestframework
- djangorestframework-simplejwt
- django-perm-filter

## Quickstart

Install Django SPA Day:

```bash
python3 -m pip install django-spaday
```

Add it to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    ...
    'django_spaday',
)
```

### Settings

In `config/urls.py` add the urls:

```python
urlpatterns = [
    path(r"djadmin/", admin.site.urls),
    ...
    path("", include("django_spaday.urls")),
]
```

In `config/api_router.py` add the API urls:

```python
urlpatterns = [
    path("", include("django_spaday.api.urls")),
    # Place all your app's API URLS here.
    ...
    path("auth/", include("dj_rest_auth.urls")),
]
```

In `config/settings/base.py` ensure your `dj-rest-auth` settings include the following:

```python
REST_AUTH = {
    "USE_JWT": True,
    "SESSION_LOGIN": False,
    "TOKEN_MODEL": None,
    "USER_DETAILS_SERIALIZER": "django_spaday.api.serializers.UserAuthSerializer",
    "JWT_AUTH_HTTPONLY": False,  # False means js can access the cookie
}
```

> NOTE: This is imporatant as it will provide the frontend app with the logged in User's permissions, etc.

### Overrides

These are the `SPA_DAY` defaults and do not need to be specified in `settings` unless you wish to override.

```python
SPA_DAY = {
    "PERMISSION_SERIALIZER": "django_spaday.api.serializers.PermissionListSerializer",
    "USER_SERIALIZER": "django_spaday.api.serializers.UserSerializer",
    "GROUP_SERIALIZER": "django_spaday.api.serializers.GroupSerializer",
    "CHANGE_PASSWORD_SERIALIZER": "django_spaday.api.serializers.ChangePasswordSerializer",
    "USER_AUTH_SERIALIZER": "django_spaday.api.serializers.UserAuthSerializer",
    "LAST_LOGIN_SERIALIZER": "django_spaday.api.serializers.LastLoginSerializer",
}
```

## Local Development

1. `make env`
1. `make pip_install`
1. `make migrations`
1. `make migrate`
1. `make superuser`
1. `make serve`

- Visit `http://127.0.0.1:8000/djadmin/` for the Django Admin
- Visit `http://127.0.0.1:8000/api/docs/` for the API docs

### Testing

Currently django_spaday has **94%** test coverage.

- Pytest: `make pytest`
- Coverage: `make coverage`
  - Open Report: `make open_coverage`

## Makefile Commands

### Environment

| Command      | Description                |
| ------------ | -------------------------- |
| `env`        | Create virtual environment |
| `env_remove` | Remove virtual environment |

### Pip

| Command       | Description          |
| ------------- | -------------------- |
| `pip_install` | install requirements |
| `pip_list`    | run pip list         |
| `pip_freeze`  | run pipfreezer       |
| `pip_checker` | run pipchecker       |

### Django

| Command      | Description                                         |
| ------------ | --------------------------------------------------- |
| `manage`     | run django manage.py (eg - make manage cmd="shell") |
| `superuser`  | Create superuser                                    |
| `migrations` | Create migrations (eg - make migrations app="core") |
| `migrate`    | Apply migrations                                    |
| `serve`      | Run server                                          |
| `show_urls`  | show urls                                           |
| `shell`      | run shell                                           |
| `flush`      | Flush database                                      |

### Testing

| Command            | Description             |
| ------------------ | ----------------------- |
| `pytest`           | Run tests               |
| `pytest_verbose`   | Run tests               |
| `coverage`         | Run tests with coverage |
| `coverage_verbose` | Run tests with coverage |
| `coverage_skip`    | Run tests with coverage |
| `open_coverage`    | open coverage report    |

### Cleanup

| Command              | Description                            |
| -------------------- | -------------------------------------- |
| `clean_build`        | remove build artifacts                 |
| `clean_pyc`          | remove python file artifacts           |
| `clean`              | remove all build and python artifacts  |
| `clean_pytest_cache` | clear pytest cache                     |
| `clean_tox_cache`    | clear tox cache                        |
| `clean_coverage`     | clear coverage cache                   |
| `clean_tests`        | clear pytest, tox, and coverage caches |

### Miscellaneous

| Command | Description         |
| ------- | ------------------- |
| `tree`  | Show directory tree |

### Deploy

| Command        | Description                     |
| -------------- | ------------------------------- |
| `dist`         | builds source and wheel package |
| `release_test` | upload package to pypi test     |
| `release`      | package and upload a release    |
