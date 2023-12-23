#una regex per identificare i worker che gestiscono i servizi
SERVICE_WORKER_NAME = r'^ServiceWorker.*$'

SERVICE_DEFAULT_QUEUE = 'service'

SERVICE_LOCK =  60 * 60 * 24 * 30 # 30 days

SERVICE_LIST = [
    
]