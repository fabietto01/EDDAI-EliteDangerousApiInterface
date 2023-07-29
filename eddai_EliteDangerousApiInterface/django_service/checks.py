from django.core.checks import register, Tags, Warning, Error

@register(Tags.compatibility)
def celery_check(app_configs, **kwargs):
    errors = []
    from django_service.settings import servis_settings
    if servis_settings.CELERY_RESULT_BACKEND is None:
        errors.append(
            Warning(
                'you must enter a RESULT BACKEND otherwise django servis is not able to work correctly',
                hint=f'put {servis_settings.DJANGO_SERVICE_CELERY_NAMESPCAE}_RESULT_BACKEND in the configurations',
                id='django_service.W001',
            )
        )
    if servis_settings.CELERY_BROKER_URL is None:
        errors.append(
            Error(
                'you must enter a BROKER URL otherwise django servis is not able to work correctly',
                hint=f'put {servis_settings.DJANGO_SERVICE_CELERY_NAMESPCAE}_BROKER_URL in the configurations',
                id='django_service.E002',
            )
        )
    if servis_settings.SERVICES_CELERY_APP is None:
        errors.append(
            Error(
                'you must enter a celery app otherwise django servis is not able to work correctly',
                hint=f'put {servis_settings.DJANGO_SERVICE_CELERY_NAMESPCAE}_APP in the configurations',
                id='django_service.E003',
            )
        )
    return errors