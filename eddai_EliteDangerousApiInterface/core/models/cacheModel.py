from django.db import models
from django.core.cache import cache

class CacheModel(models.Model):

    @classmethod
    def get_cache_key(cls, *args, **kwargs) -> str:
        args = '_'.join([str(arg) for arg in args])
        kwargs = '_'.join([f"{key}={value}" for key, value in kwargs.items()])
        if not args and not kwargs:
            return f"{cls._meta.app_label}_{cls._meta.model_name}_cache_key"
        if args and not kwargs:
            return f"{cls._meta.app_label}_{cls._meta.model_name}_cache_key_{args}"
        elif not args and kwargs:
            return f"{cls._meta.app_label}_{cls._meta.model_name}_cache_key_{kwargs}"
        else:
            return f"{cls._meta.app_label}_{cls._meta.model_name}_cache_key_{args}_{kwargs}"

    class Meta:
        abstract = True