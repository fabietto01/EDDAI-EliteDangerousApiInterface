from django.test import TestCase
from eddn.tasks import AutoAnalyticTask
from eddn.models import DataLog

from users.models import User
from django.conf import settings

class TasckTestCase(TestCase):

    fixtures = [
        'user', 'economy', 'system', 'body', 'bgs', 'exploration', 'material', 'mining', 'station',
        'eddn_test_service_event_FSDJump', 'eddn_test_service_event_Docked', 'eddn_test_service_event_Scan',
        'eddn_test_service_event_Location', 'eddn_test_service_event_SAASignalsFound', 'eddn_test_service_event_CarrierJump',
        'eddn_test_service_event_Commodity'
    ]

    @classmethod
    def setUpTestData(cls):
        user, create = User.objects.get_or_create(
            username=settings.EDDN_USER_NAME_AGENT,
        )
        user.set_password(settings.EDDN_USER_PASSWORD_AGENT)

    def test_auto_analytic(self):
        try:
            istanca = AutoAnalyticTask()
            istanca.run()
        except Exception as e:
            self.fail(f"auto_analytic() raised an exception: {e}")
        else:
            count = DataLog.objects.count()
            self.assertEqual(count, 0, f"auto_analytic() failed, {count} DataLog instances found")