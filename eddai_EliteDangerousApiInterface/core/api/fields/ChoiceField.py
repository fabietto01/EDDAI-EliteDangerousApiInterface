from rest_framework.serializers import ChoiceField, Field
from django.core.cache import cache

class CacheChoiceField(ChoiceField):
    """
    A choice field that caches the choices for a specified duration.

    This field extends the `ChoiceField` class and adds caching functionality
    to the choices. The choices are retrieved from a cache using a cache key,
    and if the choices are not found in the cache, they are generated using
    a provided function and stored in the cache for a specified duration.

    :param fun_choices: A function that returns the choices.
    :param cache_key: The cache key to use for storing and retrieving the choices, recommended to use a unique key using uuid.uuid4().
    :param kwargs: Additional keyword arguments to pass to the `ChoiceField` constructor.
    """

    def __init__(self, fun_choices, cache_key:str, **kwargs):
        choices = cache.get_or_set(cache_key, fun_choices(), 30)#60*5
        super().__init__(choices, **kwargs)