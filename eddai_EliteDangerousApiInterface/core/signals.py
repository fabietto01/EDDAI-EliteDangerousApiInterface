from django.db.models.signals import post_save, pre_delete
from django.core.cache import cache
from .models.cacheModel import CacheModel