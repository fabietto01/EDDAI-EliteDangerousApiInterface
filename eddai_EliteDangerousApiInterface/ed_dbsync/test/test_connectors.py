from django.test import TestCase

from users.models import User
from ed_dbsync.connectors.capi import CapiClient

class CapiClientTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        user = User.objects.get(username='fabietto01')
        cls.capi_clinet = CapiClient.from_task(user=user)