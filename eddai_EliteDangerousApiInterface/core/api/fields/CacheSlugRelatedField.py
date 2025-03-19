from rest_framework.serializers import SlugRelatedField 
from django.core.cache import cache


from django.db.models import Manager
from django.db.models.query import QuerySet
from django.utils.encoding import smart_str, uri_to_iri
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist

class CacheSlugRelatedField(SlugRelatedField):
    
    def to_internal_value(self, data):

        cache_key = f"{self.queryset.model._meta.label_lower}:{self.slug_field}:{data}"
        cached_object = cache.get(cache_key)


        queryset = self.get_queryset()
        try:
            return queryset.get(**{self.slug_field: data})
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field, value=smart_str(data))
        except (TypeError, ValueError):
            self.fail('invalid')
    