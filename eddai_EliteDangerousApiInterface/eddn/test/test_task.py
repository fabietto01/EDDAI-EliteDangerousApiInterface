from django.test import TestCase
from eddn.tasks import AutoAnalyticTask

class TasckTestCase(TestCase):

    fixtures = [
        'user', 'economy', 'system', 'body', 'bgs', 'exploration', 'material', 'mining', 'station',
        'eddn_test_service_event_FSDJump', 'eddn_test_service_event_Docked', 'eddn_test_service_event_Scan',
        'eddn_test_service_event_Location', 'eddn_test_service_event_SAASignalsFound', 'eddn_test_service_event_CarrierJump',
        'eddn_test_service_event_Commodity'
    ]

    def test_auto_analytic(self):
        try:
            istanca = AutoAnalyticTask()
            istanca.run()
        except Exception as e:
            self.fail(f"auto_analytic() raised an exception: {e}")
        