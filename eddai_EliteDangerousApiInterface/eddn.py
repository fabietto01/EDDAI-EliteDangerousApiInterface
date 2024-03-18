import os
import django


def main():

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eddai_EliteDangerousApiInterface.settings.default')
    django.setup()

    from .eddn.service import EddnClient

    EddnClient.connect()

if __name__ == '__main__':
    main()