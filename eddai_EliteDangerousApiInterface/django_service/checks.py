from django.core.checks import register, Tags, Warning, Error

@register(Tags.compatibility)
def celery_check(app_configs, **kwargs):
    errors = []
    from .conf import servis_settings
    return errors