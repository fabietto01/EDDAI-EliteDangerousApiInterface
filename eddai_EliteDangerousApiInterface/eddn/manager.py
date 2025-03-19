from django.db import models
from django.db.models.functions import Coalesce
from django.core.cache import cache

class EddnQuerySet(models.QuerySet):

    def cache_or_all(self, *args, **kwargs):
        
        cache_key = kwargs.pop("cache_key", None)
        if cache_key is None:
            model_name = self.model.__module__
            cache_key = f"{model_name}_eddn_qs_all"

        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return cached_result

        result = self.all()
        cache.set(cache_key, result, *args, **kwargs)
        return result

class EddnManager(models.Manager.from_queryset(EddnQuerySet)):
    pass