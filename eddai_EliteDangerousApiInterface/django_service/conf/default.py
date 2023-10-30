#impostazioni per la gestione delle code di celery
#https://docs.celeryq.dev/en/stable/userguide/routing.html
SERVICE_RELARED_NAME = r'[A-z]{1,}(service|Service)$'

SERVICE_LOCK =  60 * 60 * 24 * 30 # 30 days

SERVICE_QUEUE = None