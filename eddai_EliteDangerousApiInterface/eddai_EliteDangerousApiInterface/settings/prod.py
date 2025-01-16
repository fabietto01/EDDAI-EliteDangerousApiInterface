from .default import *
from celery.schedules import crontab

DEBUG = False

ALLOWED_HOSTS = ['*']

# Un elenco di tutte le persone che ricevono notifiche di errore del codice. 
# https://docs.djangoproject.com/en/4.1/ref/settings/#admins
ADMINS = [("Fabio Zorzetto", "fabio.zorzetto.01@gmail.com")]

#impostazione per la gestione dei taask periodici di celery
#https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-schedule
CELERY_BEAT_SCHEDULE = {
    "auto_re_analytic":{
        "task": "auto_analytic",
        "schedule": crontab(minute=0, hour=0)#crontab(minute=0, hour='*/3'),
    }
}

# The backend to use for sending emails. For the list of available backends see Sending email.
# https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-EMAIL_BACKEND
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('DJANGO_EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.environ.get('DJANGO_EMAIL_PORT', 587)
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get('DJANGO_DEFAULT_FROM_EMAIL')

# La configurazione per il framework REST è tutta con namespace all'interno di una singola impostazione Django
# https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK.update({
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
})