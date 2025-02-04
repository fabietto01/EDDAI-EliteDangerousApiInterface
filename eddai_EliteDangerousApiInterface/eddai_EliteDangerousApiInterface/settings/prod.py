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