from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.conf import settings

from .models import User

@receiver(post_save, sender=User)
def create_user_in_all_dbs(sender, instance:User, created, using, **kwargs):
    if using == 'default':
        for db in settings.DATABASES_FOR_USERS_MODEL:
            instance.save(using=db)

@receiver(pre_delete, sender=User)
def delete_user_in_all_dbs(sender, instance:User, using, **kwargs):
    if using == 'default':
        for db in settings.DATABASES_FOR_USERS_MODEL:
            instance.delete(using=db)