# Django SPA Day

A Django package that provides "out-of-the-box" basic auth, user, group, and
permission APIs for use in Single Page Apps (eg - Vue, React).

So easy, you can take a SPA day!

`django-spaday` deliberately stays below version 1.x.x to signal that every new
version may potentially have breaking changes.

## Features

- Auth
- User management w/permissions
- Group management w/permissions
- Audit Log
- Django Celery Results

## Requirements

Assumes you have started from this [cookiecutter-django](https://github.com/tsantor/cookiecutter-django) template which leverages the following.

- djangorestframework
- djangorestframework-simplejwt
- dj-rest-auth
- django-auditlog

## Quickstart

Install Django SPA Day:

```bash
pip install django-spaday
```

Add it to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    'django_spaday',
    ...
)
```

### Settings

In `config/api_router.py` add the API urls:

```
urlpatterns = [
    path("", include("django_spaday.api.urls")),
    # Place all your app's API URLS here.
    ...
]
```

In `config/settings/base.py` ensure your `dj-rest-auth` settings include the following:

```
REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "django_spaday.api.serializers.UserAuthSerializer",
    ...
}

REST_AUTH_TOKEN_MODEL = None
REST_SESSION_LOGIN = False
REST_USE_JWT = True
```

> NOTE: This is imporatant as it will provide the frontend app with the logged in User's permissions, etc.

## Development

1. `make env`
1. `python3 -m pip install -r requirements_dev.txt`
1. `python3 -m pip install -r requirements.txt`
1. `python manage.py makemigrations`
1. `python manage.py migrate`
1. `python manage.py runserver`

Visit `http://127.0.0.1:8000/djadmin/` for the Django Admin
Visit `http://127.0.0.1:8000/admin/` for the Vue Admin
