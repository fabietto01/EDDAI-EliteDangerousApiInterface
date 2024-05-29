from settings.default import *


DEBUG = False

ALLOWED_HOSTS = ['*']

# Un elenco di tutte le persone che ricevono notifiche di errore del codice. 
# https://docs.djangoproject.com/en/4.1/ref/settings/#admins
ADMINS = [("Fabio Zorzetto", "fabio.zorzetto.01@gmail.com")]


#impostazioni per la gestione delle code di celery
#https://docs.celeryq.dev/en/stable/userguide/configuration.html#broker-use-ssl
CELERY_BROKER_USE_SSL = {
    'ssl_version': ssl.PROTOCOL_TLSv1_2,
    'keyfile': os.environ.get("CELERY_SSL_KEYFILE"),
    'certfile': os.environ.get("CELERY_SSL_CERTFILE"),
    'ca_certs': os.environ.get("CELERY_SSL_CACERTFILE"),
    'cert_reqs': ssl.CERT_REQUIRED
}
#impostazione per la gestione dei taask periodici di celery
#https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-schedule
CELERY_BEAT_SCHEDULE = {
    "auto_re_analytic":{
        "task": "auto_analytic",
        "schedule": crontab(minute=0, hour=0)#crontab(minute=0, hour='*/3'),
    }
}