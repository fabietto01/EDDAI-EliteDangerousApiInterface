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

CELERY_BROKER_URL = 'memory://'
CELERY_RESULT_BACKEND = "cache+memory://"
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True