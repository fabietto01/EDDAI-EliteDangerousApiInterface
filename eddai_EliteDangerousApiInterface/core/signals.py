from django.db.models.signals import post_save, pre_delete
from django.core.cache import cache
from .models.cacheModel import CacheModel

def update_cache(sender:CacheModel, instance, **kwargs):
    cache_key = sender.get_cache_key()
    queryset = sender.objects.all()
    cache.set(cache_key, queryset)

for subclass in CacheModel.__subclasses__():
    post_save.connect(update_cache, sender=subclass)
    pre_delete.connect(update_cache, sender=subclass)