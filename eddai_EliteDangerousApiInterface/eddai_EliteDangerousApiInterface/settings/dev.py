from .default import *

INSTALLED_APPS = [
    *INSTALLED_APPS,
    "debug_toolbar",
]

# A data structure containing configuration information. When not-empty, 
# the contents of this data structure will be passed as the argument to the 
# configuration method described in LOGGING_CONFIG.
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
        "celery.task.console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "celery.task.console",
        },
        'celery.worker': {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "celery.worker.console",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.console",
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
            "handlers": ["celery.task.console", "mail_admins"],
            "level": "INFO",
            "propagate": False,
        },
        "celery.beat":{
            "handlers": ["celery.worker", "mail_admins"],
            "level": "INFO",
            "propagate": False,
        },
        "celery.worker":{
            "handlers": ["celery.worker", "mail_admins"],
            "level": "INFO",
            "propagate": False,
        },
        "eddn":{
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
            "propagate": False,
        },
        "django": {
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["console", "django.server"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    *MIDDLEWARE,
]

# Configurazione per dev container
INTERNAL_IPS = [
    "127.0.0.1",
]

# Configurazione debug toolbar per risolvere problemi JSON
DEBUG_TOOLBAR_CONFIG = {
    "RENDER_PANELS": True,
}