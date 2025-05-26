from django.test import TestCase

from ed_bgs.models import (
    MinorFaction
)

from ed_bgs.api.serializers import (
    MinorFactionBasicInformation
)

class MinorFactionSerializerTestCase(TestCase):

    fixtures = ['user', 'economy', 'system', 'bgs', 'bgs_test_data']

    def test_compacted_serializer(self):
        """
        Test the serializer for the MinorFaction model.
        """
        minor_faction = MinorFaction.objects.get(name="Mother Gaia")
        serializer = MinorFactionBasicInformation(minor_faction)
        self.assertEqual(serializer.data['id'], minor_faction.id)
        self.assertEqual(serializer.data['name'], minor_faction.name)