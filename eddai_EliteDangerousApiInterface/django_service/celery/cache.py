import time
from contextlib import contextmanager
from django.core.cache import cache
from ..conf import servis_settings

LOCK_EXPIRE = servis_settings.SERVICE_LOCK

@contextmanager
def service_lock(lock_id:str, oid):
    time_at = time.monotonic() + LOCK_EXPIRE - 3

    status = cache.add(lock_id, oid, LOCK_EXPIRE)
    try:
        yield status
    finally:
        if status:
            if time.monotonic() < time_at and status:
                cache.delete(lock_id)