"""
Django settings for eddai_EliteDangerousApiInterface project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from uuid import uuid4

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis', 

    'rest_framework', #pip install djangorestframework
    'rest_framework.authtoken', #per il login con token
    'rest_framework_gis', #pip install djangorestframework-gis
    'django_filters', #pip install django-filter
    'django_celery_beat', #pip install django-celery-beat

    'users',
    'core',

    'ed_core',
    'ed_system',
    'ed_material',
    'ed_body',
    'ed_mining',
    'ed_exploration',
    'ed_bgs',
    'ed_station',
    'ed_economy',
    
    'eddn',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'eddai_EliteDangerousApiInterface.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'eddai_EliteDangerousApiInterface.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'ed_info',
        'USER':  os.environ.get('POSTGIS_USER', "postgres"),
        'PASSWORD': os.environ.get('POSTGIS_PASSWORD', "123"),
        'HOST': os.environ.get('POSTGIS_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGIS_PORT', '5432'),
        "TEST": {
            "NAME": "ed_info_test",
            "DEPENDENCIES": [],
        },
        'OPTIONS':{
            "pool":True,
        }
    }
}

# Caches
# https://docs.djangoproject.com/en/5.1/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{os.environ.get('DJANGO_CACHES_HOST', 'localhost')}:{os.environ.get('REDIS_CACHE_PORT', '6379')}",
    }
}

# setting per la gestione della geolocalizzazione
# https://docs.djangoproject.com/en/5.0/ref/contrib/gis/install/geolibs/#geos-library-path
GDAL_LIBRARY_PATH = r'/opt/conda/lib/libgdal.so'
GEOS_LIBRARY_PATH = r'/opt/conda/lib/libgeos_c.so'

# Router per il database
# https://docs.djangoproject.com/en/5.0/ref/settings/#database-routers
DATABASE_ROUTERS = []

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static-server'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media-server'

# Directory where Django will look for fixtures
# https://docs.djangoproject.com/en/5.1/ref/settings/#fixture-dirs
# FIXTURE_DIRS = [
#     BASE_DIR / 'ed_economy/fixtures',
#     BASE_DIR / 'ed_system/fixtures',
#     BASE_DIR / 'ed_bgs/fixtures',
#     BASE_DIR / 'ed_body/fixtures',
#     BASE_DIR / 'ed_exploration/fixtures',
#     BASE_DIR / 'ed_material/fixtures',
#     BASE_DIR / 'ed_mining/fixtures',
#     BASE_DIR / 'ed_station/fixtures',
# ]

# The backend to use for sending emails. For the list of available backends see Sending email.
# https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-EMAIL_BACKEND
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-user-model
AUTH_USER_MODEL = 'users.User'

# La configurazione per il framework REST è tutta con namespace all'interno di una singola impostazione Django
# https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 500,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ]
}

# Struttura dati contenente informazioni di configurazione. 
# Quando non è vuoto, il Il contenuto di questa struttura di dati 
# verrà passato come argomento al Metodo di configurazione descritto in LOGGING_CONFIG.
# https://docs.djangoproject.com/en/4.1/ref/settings/#logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
        "django.console":{
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
        "celery.task.console": {
            "()": "celery.app.log.TaskFormatter",
            "format": "%(asctime)s [%(levelname)s] [%(processName)s] [%(task_name)s(%(task_id)s)] %(message)s",
        },
        "celery.worker.console": {
            "()": "celery.utils.log.ColorFormatter",
            "format": "%(asctime)s [%(levelname)s] [%(processName)s] %(message)s",
        },
    },
    "handlers": {
        "celery.task.console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "celery.task.console",
        },
        'celery.worker': {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "celery.worker.console",
        },
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "django.console",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "celery.task":{
            "handlers": ["celery.task.console", "mail_admins"],
            "level": "INFO",
        },
        "celery.beat":{
            "handlers": ["celery.worker", "mail_admins"],
            "level": "INFO",
        },
        "celery.worker":{
            "handlers": ["celery.worker", "mail_admins"],
            "level": "INFO",
        },
        "eddn":{
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
        },
        "django": {
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

#impostazioni deticatte al app EDDN pre la sinc del database con i datti 
# provenienti dalla community ED
EDDN_RELY = "tcp://eddn.edcd.io:9500"
EDDN_TIMEOUT = 600000
AUTHORI_SED_SOFTWARS = [
    "E:D Market Connector",
    "E:D Market Connector [Windows]",
    "EDDiscovery",
    "EDDI",
    "EDCE",
    "ED-TD.SPACE",
    "EliteOCR",
    "Maddavo's Market Share",
    "RegulatedNoise",
    "RegulatedNoise__DJ"
]

#impostazioni per la gestione dell'utente nominativa per il scrivere i datti su DB, da parte del servizio EDDN
EDDN_USER_NAME_AGENT = os.environ.get('EDDN_USER_NAME_AGENT', "EDDN-Client")
EDDN_USER_PASSWORD_AGENT = os.environ.get('EDDN_USER_PASSWORD_AGENT', 'password!123')

#impostazioni per la gestione delle code di celery
#https://docs.celeryq.dev/en/stable/userguide/configuration.html
CELERY_BROKER_URL = F'amqp://{os.environ.get("CELERY_BROKER_USER")}:{os.environ.get("CELERY_BROKER_PASSWORD")}@{os.environ.get("CELERY_BROKER_HOST")}:5672/{os.environ.get("CELERY_BROKER_VHOST")}'
CELERY_RESULT_BACKEND =  F'redis://{os.environ.get("CELERY_RESULT_BACKEND_HOST")}:{os.environ.get("CELERY_RESULT_BACKEND_PORT")}'

#impostazioni per la gestione della serializzazione dei dati
#https://docs.celeryq.dev/en/stable/userguide/calling.html#serializers
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_EVENT_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['application/json', 'application/x-python-serialize']

#impostazioni per la gestione delle code predefinata di celery
#https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-task_default_queue
CELERY_TASK_DEFAULT_QUEUE = 'default'

#impostazione per la gestione delle code dei task di celery
#https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-task_queues
from kombu import Queue
CELERY_TASK_QUEUES = (
    Queue('default', routing_key='task.#'),
    Queue('eddn', routing_key='service.eddn'),
    Queue('admin', routing_key='admin.#'),
)

#impostazione per la gestione dei ruting dei tasck di celery
#https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-routes
CELERY_TASK_ROUTES = {
    "service.eddn": {
        "queue": "eddn",
        "routing_key": "service.eddn",
    }
}