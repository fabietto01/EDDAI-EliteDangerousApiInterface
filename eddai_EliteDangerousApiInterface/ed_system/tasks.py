from celery import shared_task

from .models import System

import time

@shared_task
def create_system():
    print('elaborazione in corso')
    System.objects.get_or_create(
        name='celery_test',
        defaults={
            'x': 0,
            'y': 0,
            'z': 0,
            'population': 0,

        }
    )
    print('elaborazione terminata')

@shared_task
def test():
    time.sleep(10)
    print('test')