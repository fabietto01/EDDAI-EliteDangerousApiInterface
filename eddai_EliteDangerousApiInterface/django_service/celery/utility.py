import time
from contextlib import contextmanager
from django.core.cache import cache

from ..conf import servis_settings

TIMEOUT_CACHE = servis_settings.SERVICE_TIMEOUT_CACHE

@contextmanager
def memcache_lock(lock_id, oid, timeout=TIMEOUT_CACHE):
    """
    Context manager for acquiring and releasing a memcache lock.

    Args:
        lock_id (str): The identifier for the lock.
        oid (str): The identifier for the object being locked.
        timeout (int, optional): The timeout for the lock in seconds. Defaults to TIMEOUT_CACHE.

    Yields:
        bool: The status of acquiring the lock.

    """
    timeout_at = time.monotonic() + timeout - 3
    status = cache.add(lock_id, oid, timeout)
    try:
        yield status
    finally:
        if time.monotonic() < timeout_at and status:
            cache.delete(lock_id)