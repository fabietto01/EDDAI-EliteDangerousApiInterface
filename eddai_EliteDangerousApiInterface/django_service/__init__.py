try:
    import django
except ImportError: 
    raise ImportError("Django is not installed. Please install Django and try again.")

try:
    import celery 
except ImportError:
    raise ImportError("Celery is not installed. Please install Celery and try again.")


if django.VERSION < (3, 2):
    default_app_config = 'django_service.apps.DjangoServiceConfig'

__title__ = 'Django service'
__version__ = '0.0.1'
__author__ = 'Fabio Zorzetto'
__license__ = None
__copyright__ = None

from celery import Celery
from .utility import get_celery_app

app:Celery = get_celery_app()

# Version synonym
VERSION = __version__