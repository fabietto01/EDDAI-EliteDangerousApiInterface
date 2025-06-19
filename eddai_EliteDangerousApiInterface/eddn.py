#!/usr/bin/env python
import os

def main():
    """
    Entry point of the program.
    
    This function sets up the Django environment, imports the EddnClient module,
    and connects to the EddnClient.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eddai_EliteDangerousApiInterface.settings.default')
    
    try:
        import django
        django.setup()
    except ImportError as e:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from e
    
    try:
        from ed_dbsync.service import EddnClient
    except ImportError as e:
        raise ImportError(
            "Couldn't import EddnClient. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from e

    client = EddnClient()
    client.connect()

if __name__ == '__main__':
    main()