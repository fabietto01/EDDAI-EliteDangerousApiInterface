from eddai_EliteDangerousApiInterface.settings.default import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'ed_info':{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ed_info-eddn',
        'USER': 'ed_info-dev-user',
        'PASSWORD': 'vkWCRnO7$oOLCm^ZNd#P@1*Pgbch7wPAMgm3Knd1FrRD&SH5DS',
        'HOST': '129.152.2.89',
        'PORT': '3306',
    }
}