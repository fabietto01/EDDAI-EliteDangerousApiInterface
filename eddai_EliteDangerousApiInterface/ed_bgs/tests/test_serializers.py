from django.test import TestCase

from ed_bgs.models import (
    Faction, Government, State, PowerState, Power,
    MinorFaction, MinorFactionInSystem, StateInMinorFaction,
    PowerInSystem
)

from ed_bgs.api.serializers import (
    FactionBasicInformationSerializer, FactionSerializer,
    GovernmentBasicInformationSerializer, GovernmentSerializer,
    StateBasicInformationSerializer, StateSerializer,
    PowerStateBasicInformationSerializer, PowerStateSerializer,
    PowerBasicInformationSerializer, PowerSerializer,
    MinorFactionBasicInformation, MinorFactionSerializer,
    MinorFactionInSystemBasicInformationSerializer,
    MinorFactionInSystemSerializer,
    MinorFactionInSystemFromMinorFactionSerializer,
    MinorFactionInSystemFromsystemSerializer,
    StateInMinorFactionSerializer,
    PowerInSystemBasicInformationSerializer,
    PowerInSystemSerializer,
    PowerInSystemFromSystemSerializer,
)
from users.models import User


class FactionSerializerTestCase(TestCase):
    
    fixtures = ['user', 'economy', 'system', 'bgs']

    def test_faction_basic_information_serializer(self):
        """Test the basic information serializer for Faction."""
        faction = Faction.objects.first()
        serializer = FactionBasicInformationSerializer(faction)
        self.assertEqual(serializer.data['id'], faction.id)
        self.assertEqual(serializer.data['name'], faction.name)
        self.assertEqual(len(serializer.data.keys()), 2)

    def test_faction_serializer(self):
        """Test the detailed serializer for Faction."""
        faction = Faction.objects.first()
        serializer = FactionSerializer(faction)
        self.assertEqual(serializer.data['id'], faction.id)
        self.assertEqual(serializer.data['name'], faction.name)
        self.assertNotIn('_eddn', serializer.data)
        self.assertNotIn('eddn', serializer.data)


class GovernmentSerializerTestCase(TestCase):
    
    fixtures = ['user', 'economy', 'system', 'bgs']

    def test_government_basic_information_serializer(self):
        """Test the basic information serializer for Government."""
        government = Government.objects.first()
        serializer = GovernmentBasicInformationSerializer(government)
        self.assertEqual(serializer.data['id'], government.id)
        self.assertEqual(serializer.data['name'], government.name)
        self.assertEqual(len(serializer.data.keys()), 2)

    def test_government_serializer(self):
        """Test the detailed serializer for Government."""
        government = Government.objects.first()
        serializer = GovernmentSerializer(government)
        self.assertEqual(serializer.data['id'], government.id)
        self.assertEqual(serializer.data['name'], government.name)
        self.assertNotIn('_eddn', serializer.data)
        self.assertNotIn('eddn', serializer.data)


class StateSerializerTestCase(TestCase):
    
    fixtures = ['user', 'economy', 'system', 'bgs']

    def test_state_basic_information_serializer(self):
        """Test the basic information serializer for State."""
        state = State.objects.first()
        serializer = StateBasicInformationSerializer(state)
        self.assertEqual(serializer.data['id'], state.id)
        self.assertEqual(serializer.data['name'], state.name)
        self.assertEqual(len(serializer.data.keys()), 2)

    def test_state_serializer(self):
        """Test the detailed serializer for State."""
        state = State.objects.first()
        serializer = StateSerializer(state)
        self.assertEqual(serializer.data['id'], state.id)
        self.assertEqual(serializer.data['name'], state.name)
        self.assertNotIn('_eddn', serializer.data)
        self.assertNotIn('eddn', serializer.data)


class PowerStateSerializerTestCase(TestCase):
    
    fixtures = ['user', 'economy', 'system', 'bgs']

    def test_powerstate_basic_information_serializer(self):
        """Test the basic information serializer for PowerState."""
        powerstate = PowerState.objects.first()
        serializer = PowerStateBasicInformationSerializer(powerstate)
        self.assertEqual(serializer.data['id'], powerstate.id)
        self.assertEqual(serializer.data['name'], powerstate.name)
        self.assertEqual(len(serializer.data.keys()), 2)

    def test_powerstate_serializer(self):
        """Test the detailed serializer for PowerState."""
        powerstate = PowerState.objects.first()
        serializer = PowerStateSerializer(powerstate)
        self.assertEqual(serializer.data['id'], powerstate.id)
        self.assertEqual(serializer.data['name'], powerstate.name)
        self.assertNotIn('_eddn', serializer.data)
        self.assertNotIn('eddn', serializer.data)


class PowerSerializerTestCase(TestCase):
    
    fixtures = ['user', 'economy', 'system', 'bgs']

    def test_power_basic_information_serializer(self):
        """Test the basic information serializer for Power."""
        power = Power.objects.first()
        serializer = PowerBasicInformationSerializer(power)
        self.assertEqual(serializer.data['id'], power.id)
        self.assertEqual(serializer.data['name'], power.name)
        self.assertEqual(len(serializer.data.keys()), 2)

    def test_power_serializer(self):
        """Test the detailed serializer for Power."""
        power = Power.objects.first()
        serializer = PowerSerializer(power)
        self.assertEqual(serializer.data['id'], power.id)
        self.assertEqual(serializer.data['name'], power.name)
        if power.headquarter:
            self.assertEqual(serializer.data['headquarter'], power.headquarter.name)
        if power.allegiance:
            self.assertEqual(serializer.data['allegiance'], power.allegiance.name)


class MinorFactionSerializerTestCase(TestCase):

    fixtures = ['user', 'economy', 'system', 'bgs', 'bgs_test_data']

    def test_minor_faction_basic_information(self):
        """Test the basic information serializer for MinorFaction."""
        minor_faction = MinorFaction.objects.get(name="Mother Gaia")
        serializer = MinorFactionBasicInformation(minor_faction)
        self.assertEqual(serializer.data['id'], minor_faction.id)
        self.assertEqual(serializer.data['name'], minor_faction.name)
        self.assertEqual(len(serializer.data.keys()), 2)

    def test_minor_faction_serializer(self):
        """Test the detailed serializer for MinorFaction."""
        minor_faction = MinorFaction.objects.get(name="Mother Gaia")
        serializer = MinorFactionSerializer(minor_faction)
        self.assertEqual(serializer.data['id'], minor_faction.id)
        self.assertEqual(serializer.data['name'], minor_faction.name)
        self.assertEqual(serializer.data['allegiance'], minor_faction.allegiance.name)
        self.assertEqual(serializer.data['government'], minor_faction.government.name)
        self.assertIn('created_at', serializer.data)
        self.assertIn('updated_at', serializer.data)


class MinorFactionInSystemSerializerTestCase(TestCase):

    fixtures = ['user', 'economy', 'system', 'bgs', 'bgs_test_data']

    def setUp(self):
        from ed_system.models import System
        self.user = User.objects.first()
        self.system = System.objects.first()
        self.minor_faction = MinorFaction.objects.first()
        self.mfis = MinorFactionInSystem.objects.create(
            system=self.system,
            minorFaction=self.minor_faction,
            Influence=0.5,
            created_by=self.user,
            updated_by=self.user,
        )

    def test_minor_faction_in_system_basic_serializer(self):
        """Test the basic information serializer for MinorFactionInSystem."""
        serializer = MinorFactionInSystemBasicInformationSerializer(self.mfis)
        self.assertEqual(serializer.data['id'], self.mfis.id)
        self.assertEqual(serializer.data['system'], self.mfis.system.name)
        self.assertEqual(serializer.data['minorFaction'], self.mfis.minorFaction.name)
        self.assertEqual(float(serializer.data['Influence']), self.mfis.Influence)

    def test_minor_faction_in_system_serializer(self):
        """Test the detailed serializer for MinorFactionInSystem."""
        serializer = MinorFactionInSystemSerializer(self.mfis)
        self.assertEqual(serializer.data['id'], self.mfis.id)
        self.assertEqual(serializer.data['system'], self.mfis.system.name)
        self.assertEqual(serializer.data['minorFaction'], self.mfis.minorFaction.name)
        self.assertIn('states', serializer.data)

    def test_minor_faction_in_system_from_minor_faction_serializer(self):
        """Test serializer for MinorFactionInSystem from MinorFaction perspective."""
        serializer = MinorFactionInSystemFromMinorFactionSerializer(self.mfis)
        self.assertEqual(serializer.data['id'], self.mfis.id)
        self.assertEqual(serializer.data['system'], self.mfis.system.name)
        self.assertNotIn('minorFaction', serializer.data)

    def test_minor_faction_in_system_from_system_serializer(self):
        """Test serializer for MinorFactionInSystem from System perspective."""
        serializer = MinorFactionInSystemFromsystemSerializer(self.mfis)
        self.assertEqual(serializer.data['id'], self.mfis.id)
        self.assertEqual(serializer.data['minorFaction'], self.mfis.minorFaction.name)
        self.assertNotIn('system', serializer.data)


class StateInMinorFactionSerializerTestCase(TestCase):

    fixtures = ['user', 'economy', 'system', 'bgs', 'bgs_test_data']

    def setUp(self):
        from ed_system.models import System
        self.user = User.objects.first()
        self.system = System.objects.first()
        self.minor_faction = MinorFaction.objects.first()
        self.state = State.objects.first()
        self.mfis = MinorFactionInSystem.objects.create(
            system=self.system,
            minorFaction=self.minor_faction,
            Influence=0.5,
            created_by=self.user,
            updated_by=self.user,
        )
        self.simf = StateInMinorFaction.objects.create(
            minorFaction=self.mfis,
            state=self.state,
            phase='A',
            created_by=self.user,
            updated_by=self.user,
        )

    def test_state_in_minor_faction_serializer(self):
        """Test the serializer for StateInMinorFaction."""
        serializer = StateInMinorFactionSerializer(self.simf)
        self.assertEqual(serializer.data['id'], self.simf.id)
        self.assertEqual(serializer.data['state'], self.simf.state.name)
        self.assertIn('phase', serializer.data)
        self.assertNotIn('minorFaction', serializer.data)


class PowerInSystemSerializerTestCase(TestCase):

    fixtures = ['user', 'economy', 'system', 'bgs']

    def setUp(self):
        from ed_system.models import System
        self.user = User.objects.first()
        self.system = System.objects.first()
        self.power = Power.objects.first()
        self.powerstate = PowerState.objects.first()
        self.pis = PowerInSystem.objects.create(
            system=self.system,
            power=self.power,
            state=self.powerstate,
            created_by=self.user,
            updated_by=self.user,
        )

    def test_power_in_system_basic_serializer(self):
        """Test the basic information serializer for PowerInSystem."""
        serializer = PowerInSystemBasicInformationSerializer(self.pis)
        self.assertEqual(serializer.data['id'], self.pis.id)
        self.assertEqual(serializer.data['system'], self.pis.system.name)
        self.assertEqual(serializer.data['power'], self.pis.power.name)
        self.assertEqual(serializer.data['state'], self.pis.state.name)

    def test_power_in_system_serializer(self):
        """Test the detailed serializer for PowerInSystem."""
        serializer = PowerInSystemSerializer(self.pis)
        self.assertEqual(serializer.data['id'], self.pis.id)
        self.assertEqual(serializer.data['system'], self.pis.system.name)
        self.assertEqual(serializer.data['power'], self.pis.power.name)
        self.assertEqual(serializer.data['state'], self.pis.state.name)

    def test_power_in_system_from_system_serializer(self):
        """Test serializer for PowerInSystem from System perspective."""
        serializer = PowerInSystemFromSystemSerializer(self.pis)
        self.assertEqual(serializer.data['id'], self.pis.id)
        self.assertEqual(serializer.data['power'], self.pis.power.name)
        self.assertEqual(serializer.data['state'], self.pis.state.name)
        self.assertNotIn('system', serializer.data)