from django.conf import settings
# Import from `django.core.signals` instead of the official location
# `django.test.signals` to avoid importing the test module unnecessarily.
from django.core.signals import setting_changed
from django.utils.module_loading import import_string

from . import default as DEFAULTS

def get_default_kay() -> list[str]:
    return [kay for kay in dir(DEFAULTS) if kay.isupper()]

def get_default_dict() -> dict:
    return {
        string: getattr(DEFAULTS, string) for string in get_default_kay()
    } 

IMPORT_STRINGS = []

# List of settings that have been removed
REMOVED_SETTINGS = []

def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        return import_string(val)
    except ImportError as e:
        msg = "Could not import '%s' for API setting '%s'. %s: %s." % (val, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)

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

class ServiceSettings:
    """
    Class used to access django_service settings, with the appropriate
    defaults applied.
    """

    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)
        self.defaults = defaults or get_default_dict()
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings =  {
                key: getattr(settings, key) for key in get_default_kay() if hasattr(settings, key)
            }
        return self._user_settings
        
    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid django_service setting: '%s'" % attr)

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
        """
        Check that user settings are correct and return them formatted correctly.
        """
        SETTINGS_DOC = ""
        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                raise RuntimeError("The '%s' setting has been removed. Please refer to '%s' for available settings." % (setting, SETTINGS_DOC))
        return user_settings
    
    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, '_user_settings'):
            delattr(self, '_user_settings')


servis_settings = ServiceSettings(None, get_default_dict(), IMPORT_STRINGS)


def reload_servis_settings(*args, **kwargs):
    setting = kwargs['setting']
    if setting in get_default_kay():
        servis_settings.reload()


setting_changed.connect(reload_servis_settings)