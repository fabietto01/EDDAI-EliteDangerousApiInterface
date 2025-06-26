from .default import *
from celery.schedules import crontab

DEBUG = False

ALLOWED_HOSTS = ['*']

# Un elenco di tutte le persone che ricevono notifiche di errore del codice. 
# https://docs.djangoproject.com/en/4.1/ref/settings/#admins
ADMINS = [("Fabio Zorzetto", "fabio.zorzetto.01@gmail.com")]

#impostazione per la gestione dei taask periodici di celery
#https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-schedule
CELERY_BEAT_SCHEDULE = {}

# The backend to use for sending emails. For the list of available backends see Sending email.
# https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-EMAIL_BACKEND
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('DJANGO_EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.environ.get('DJANGO_EMAIL_PORT', 587)
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get('DJANGO_DEFAULT_FROM_EMAIL')

# Struttura dati contenente informazioni di configurazione. 
# Quando non è vuoto, il Il contenuto di questa struttura di dati 
# verrà passato come argomento al Metodo di configurazione descritto in LOGGING_CONFIG.
# https://docs.djangoproject.com/en/4.1/ref/settings/#logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
        "django.console":{
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
        "celery.task.console": {
            "()": "celery.app.log.TaskFormatter",
            "format": "[%(asctime)s] [%(levelname)s] [CELERY-TASK] [%(task_name)s(%(task_id)s)] %(message)s",
        },
        "celery.worker.console": {
            "()": "celery.utils.log.ColorFormatter",
            "format": "[%(asctime)s] [%(levelname)s] [CELERY-WORKER] %(message)s",
        },
    },
    "handlers": {
        "celery.task.loki": {
            "level": "INFO",
            "class": "logging_loki.LokiHandler",
            "formatter": "celery.task.console",
            "url": f"http://{os.environ.get('LOKI_HOST', 'localhost')}:{os.environ.get('LOKI_PORT', '3100')}/loki/api/v1/push",
            "tags": {"application": "eddai_EliteDangerousApiInterface", "service": "celery.task"},
            "version": "1",
        },
        "celery.worker.loki": {
            "level": "INFO",
            "class": "logging_loki.LokiHandler",
            "formatter": "celery.task.console",
            "url": f"http://{os.environ.get('LOKI_HOST', 'localhost')}:{os.environ.get('LOKI_PORT', '3100')}/loki/api/v1/push",
            "tags": {"application": "eddai_EliteDangerousApiInterface", "service": "celery.worker"},
            "version": "1",
        },
        "celery.beat.loki": {
            "level": "INFO",
            "class": "logging_loki.LokiHandler",
            "formatter": "celery.task.console",
            "url": f"http://{os.environ.get('LOKI_HOST', 'localhost')}:{os.environ.get('LOKI_PORT', '3100')}/loki/api/v1/push",
            "tags": {"application": "eddai_EliteDangerousApiInterface", "service": "celery.beat"},
            "version": "1",
        },
        "eddn.loki": {
            "level": "INFO",
            "class": "logging_loki.LokiHandler",
            "formatter": "celery.task.console",
            "url": f"http://{os.environ.get('LOKI_HOST', 'localhost')}:{os.environ.get('LOKI_PORT', '3100')}/loki/api/v1/push",
            "tags": {"application": "eddai_EliteDangerousApiInterface", "service": "eddn"},
            "version": "1",
        },
        "django.loki": {
            "level": "INFO",
            "class": "logging_loki.LokiHandler",
            "formatter": "celery.task.console",
            "url": f"http://{os.environ.get('LOKI_HOST', 'localhost')}:{os.environ.get('LOKI_PORT', '3100')}/loki/api/v1/push",
            "tags": {"application": "eddai_EliteDangerousApiInterface", "service": "django"},
            "version": "1",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {
            "level": "CRITICAL",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "celery.task":{
            "handlers": ["celery.task.loki", "mail_admins"],
            "level": "INFO",
        },
        "celery.beat":{
            "handlers": ["celery.beat.loki", "mail_admins"],
            "level": "INFO",
        },
        "celery.worker":{
            "handlers": ["celery.worker.loki", "mail_admins"],
            "level": "INFO",
        },
        "eddn":{
            "handlers": ["eddn.loki", "mail_admins"],
            "level": "INFO",
        },
        "django": {
            "handlers": ["django.loki", "mail_admins"],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["django.loki", "django.server"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# La configurazione per il framework REST è tutta con namespace all'interno di una singola impostazione Django
# https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK.update({
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
})

# The URL where requests are redirected for login, especially when using the login_required() decorator.
#https://docs.djangoproject.com/en/5.1/ref/settings/#csrf-failure-view
CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'

# A list of strings representing the host/domain names that this Django site can serve.
# https://docs.djangoproject.com/en/5.1/ref/settings/#csrf-trusted-origins
CSRF_TRUSTED_ORIGINS = [
    'https://eddai.italiangamingsystem.it'
]

# Cacheops
# https://github.com/Suor/django-cacheops?tab=readme-ov-file#setup
CACHEOPS_DEGRADE_ON_FAILURE = True