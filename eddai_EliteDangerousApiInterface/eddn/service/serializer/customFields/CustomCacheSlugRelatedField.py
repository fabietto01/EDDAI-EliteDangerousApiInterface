from .BaseCustinField import BaseCustomField
from core.api.fields import CacheSlugRelatedField

from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.utils.encoding import smart_str, uri_to_iri

class CustomCacheSlugRelatedField(CacheSlugRelatedField, BaseCustomField):
        
    def run_validation(self, data):
        data = BaseCustomField._to_internal_value(self, data)
        return super().run_validation(data)