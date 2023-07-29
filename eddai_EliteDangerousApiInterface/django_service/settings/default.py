CELERY_BROKER_URL = None
CELERY_RESULT_BACKEND = None

SERVICES_CELERY_APP = None

SERVICE_RELARED_NAME = 'service'

#impostazioni per la gestione delle code di celery
#https://docs.celeryq.dev/en/stable/userguide/routing.html
SERVICE_ROUTING_RE = r'[A-z]{1,}(service|Service)$'