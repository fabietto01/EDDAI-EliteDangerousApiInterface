from eddai_EliteDangerousApiInterface.settings.default import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'ed_info':{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ed_info-dev',
        'USER': 'ed_info-user',
        'PASSWORD': os.environ.get('MYSQL_USER_ED_INFO_PASSWORD', "vkWCRnO7$oOLCm^ZNd#P@1*Pgbch7wPAMgm3Knd1FrRD&SH5DS"),
        'HOST': os.environ.get('MYSQL_HOST', 'localhost'),
        'PORT': '3306',
    }
}