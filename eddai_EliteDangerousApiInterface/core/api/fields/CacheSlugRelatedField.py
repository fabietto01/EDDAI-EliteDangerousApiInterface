from rest_framework.serializers import SlugRelatedField 
from django.core.cache import cache

class CacheSlugRelatedField(SlugRelatedField):
    """
    A custom field that extends `SlugRelatedField` to add caching functionality for 
    improved performance when resolving related objects by their slug field.
    This field caches the resolved object using a cache key constructed from the 
    model's label, the slug field name, and the provided slug value. If the object 
    is found in the cache, it is returned directly, bypassing the database query. 
    Otherwise, the object is resolved using the parent class's `to_internal_value` 
    method, and the result is stored in the cache for future lookups.
    Attributes:
        slug_field (str): The name of the slug field used to resolve the related object.
        queryset (QuerySet): The queryset used to look up the related object.
    Methods:
        to_internal_value(data):
            Resolves the related object by its slug value, utilizing caching to 
            optimize performance.
    """

    def __init__(self, timeout=None, **kwargs):
        self.timeout = timeout
        super().__init__(**kwargs)
    
    def to_internal_value(self, data):

        cache_key = f"{self.queryset.model._meta.label_lower}:{self.slug_field}:{data}"
        cached_object = cache.get(cache_key)

        if cached_object:
            return cached_object
        
        instance = super().to_internal_value(data)

        cache.set(cache_key, instance, self.timeout)

        return instance