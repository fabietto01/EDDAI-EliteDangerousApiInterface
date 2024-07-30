from django.db import models
from django.core.cache import cache

class CacheModel(models.Model):

    @classmethod
    def get_cache_key(cls) -> str:
        return f"{cls._meta.app_label}_{cls._meta.model_name}_cache_key"
    
    class Meta:
        abstract = True