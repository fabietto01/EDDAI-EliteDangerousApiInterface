from django.core.checks import register, Warning
from django.conf import settings


@register("users", deploy=True)
def checks_app_users(app_configs, **kwargs):
    errors = []
    if getattr(settings, 'DATABASES_FOR_USERS_MODEL', []) is []:
        errors.append(
            Warning("DATABASES_FOR_USERS_MODEL is empty", hint="You should set DATABASES_FOR_USERS_MODEL in settings.py", obj="settings.py", id="users.W001")
        )
    return errors