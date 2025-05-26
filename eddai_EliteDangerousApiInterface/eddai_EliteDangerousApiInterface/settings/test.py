from .default import *

DEBUG = False

ALLOWED_HOSTS = ['*']

# Un elenco di tutte le persone che ricevono notifiche di errore del codice. 
# https://docs.djangoproject.com/en/4.1/ref/settings/#admins
ADMINS = [("Fabio Zorzetto", "fabio.zorzetto.01@gmail.com")]

# Caches
# https://docs.djangoproject.com/en/5.1/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

# Cacheops
# https://github.com/Suor/django-cacheops?tab=readme-ov-file#setup
CACHEOPS_ENABLED = False

#impostazioni per la gestione delle code di celery
#https://docs.celeryq.dev/en/stable/userguide/configuration.html
CELERY_BROKER_URL = 'memory://'
CELERY_RESULT_BACKEND = "cache+memory://"

# impostazioni per la gestione dei task di celery in modalità sincrona
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-always-eager
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True