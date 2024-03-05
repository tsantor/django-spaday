"""
Settings for Django SPA Day are all namespaced in the SPA_DAY setting.
For example your project's `settings.py` file might look like this:

SPA_DAY = {
    "PERMISSION_SERIALIZER": "django_spaday.api.serializers.PermissionListSerializer",
    "USER_SERIALIZER": "django_spaday.api.serializers.UserSerializer",
    "GROUP_SERIALIZER": "django_spaday.api.serializers.GroupSerializer",
    "CHANGE_PASSWORD_SERIALIZER": "django_spaday.api.serializers.ChangePasswordSerializer",
    "USER_AUTH_SERIALIZER": "django_spaday.api.serializers.UserAuthSerializer",
    "LAST_LOGIN_SERIALIZER": "django_spaday.api.serializers.LastLoginSerializer",
}

This module provides the `api_setting` object, that is used to access
Django SPA Day settings, checking for user settings first, then falling
back to the defaults.
"""

from django.conf import settings
from django.test.signals import setting_changed
from django.utils.module_loading import import_string

DEFAULTS = {
    "PERMISSION_SERIALIZER": "django_spaday.api.serializers.PermissionListSerializer",
    "USER_SERIALIZER": "django_spaday.api.serializers.UserSerializer",
    "GROUP_SERIALIZER": "django_spaday.api.serializers.GroupSerializer",
    "CHANGE_PASSWORD_SERIALIZER": "django_spaday.api.serializers.ChangePasswordSerializer",
    "USER_AUTH_SERIALIZER": "django_spaday.api.serializers.UserAuthSerializer",
    "LAST_LOGIN_SERIALIZER": "django_spaday.api.serializers.LastLoginSerializer",
}


# List of settings that may be in string import notation.
IMPORT_STRINGS = [
    "PERMISSION_SERIALIZER",
    "USER_SERIALIZER",
    "GROUP_SERIALIZER",
    "CHANGE_PASSWORD_SERIALIZER",
    "USER_AUTH_SERIALIZER",
    "LAST_LOGIN_SERIALIZER",
]


# List of settings that have been removed
REMOVED_SETTINGS = []


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, str):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        return import_string(val)
    except ImportError as e:
        msg = "Could not import '{}' for API setting '{}'. {}: {}.".format(
            val,
            setting_name,
            e.__class__.__name__,
            e,
        )
        raise ImportError(msg)


class APISettings:
    """
    A settings object that allows Django SPA Day settings to be accessed as
    properties. For example:

        from django_spaday.settings import api_settings
        print(api_settings.IP_GEO_HANDLER)

    Any setting with string import paths will be automatically resolved
    and return the class, rather than the string literal.

    Note:
    This is an internal class that is only compatible with settings namespaced
    under the SPA_DAY name. It is not intended to be used by 3rd-party
    apps, and test helpers like `override_settings` may not work as expected.
    """

    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, "SPA_DAY", {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid API setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def __check_user_settings(self, user_settings):
        SETTINGS_DOC = "TODO"
        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                raise RuntimeError(
                    "The '%s' setting has been removed. Please refer to '%s' for available settings."
                    % (setting, SETTINGS_DOC)
                )
        return user_settings

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, "_user_settings"):
            delattr(self, "_user_settings")


api_settings = APISettings(None, DEFAULTS, IMPORT_STRINGS)


def reload_api_settings(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == "SPA_DAY":
        api_settings.reload()


setting_changed.connect(reload_api_settings)
