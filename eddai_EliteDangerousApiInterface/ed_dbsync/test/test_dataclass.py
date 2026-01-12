"""
Test suite per la dataclass IncomingData.
Verifica che gli oggetti possano essere serializzati/deserializzati correttamente
per l'uso con Celery e che tutti gli attributi siano preservati.
"""
import json
import pickle
from dataclasses import asdict
from django.test import TestCase

from ed_dbsync.dataclass import IncomingData


class IncomingDataTestCase(TestCase):
    """Test case per la dataclass IncomingData."""

    def setUp(self):
        """Setup dei dati di test."""
        self.test_data = {
            '$schemaRef': 'https://eddn.edcd.io/schemas/commodity/3',
            'header': {
                'gamebuild': '',
                'gameversion': 'CAPI-Live-market',
                'gatewayTimestamp': '2026-01-12T04:04:10.261515Z',
                'softwareName': 'E:D Market Connector [Windows]',
                'softwareVersion': '6.0.2',
                'uploaderID': 'fe553b64504b508767497ec2c0bcbc6fbe89bb54'
            },
            'message': {
                'commodities': [
                    {
                        'buyPrice': 0,
                        'demand': 773221,
                        'demandBracket': 3,
                        'meanPrice': 2863,
                        'name': 'advancedcatalysers',
                        'sellPrice': 3472,
                        'stock': 0,
                        'stockBracket': 0
                    }
                ]
            }
        }

    def test_incoming_data_creation(self):
        """Test che l'oggetto IncomingData possa essere creato correttamente."""
        incoming = IncomingData(source='eddn', data=self.test_data)
        
        # Verifica che l'oggetto sia stato creato
        self.assertIsNotNone(incoming)
        self.assertEqual(incoming.source, 'eddn')
        self.assertEqual(incoming.data, self.test_data)

    def test_incoming_data_has_guid(self):
        """Test che l'oggetto IncomingData abbia l'attributo guid."""
        incoming = IncomingData(source='eddn', data=self.test_data)
        
        # Verifica che guid esista ed sia una stringa non vuota
        self.assertTrue(hasattr(incoming, 'guid'))
        self.assertIsInstance(incoming.guid, str)
        self.assertGreater(len(incoming.guid), 0)

    def test_incoming_data_guid_is_unique(self):
        """Test che ogni istanza abbia un guid unico."""
        incoming1 = IncomingData(source='eddn', data=self.test_data)
        incoming2 = IncomingData(source='eddn', data=self.test_data)
        
        # I guid devono essere diversi
        self.assertNotEqual(incoming1.guid, incoming2.guid)

    def test_incoming_data_pickle_serialization(self):
        """
        Test che l'oggetto IncomingData possa essere serializzato e deserializzato con pickle.
        Questo è il metodo di serializzazione predefinito di Celery.
        """
        # Crea l'oggetto originale
        original = IncomingData(source='eddn', data=self.test_data)
        original_guid = original.guid
        
        # Serializza con pickle (come fa Celery)
        serialized = pickle.dumps(original)
        
        # Deserializza
        deserialized = pickle.loads(serialized)
        
        # Verifica che tutti gli attributi siano preservati
        self.assertEqual(deserialized.source, original.source)
        self.assertEqual(deserialized.data, original.data)
        self.assertEqual(deserialized.guid, original_guid)
        self.assertTrue(hasattr(deserialized, 'guid'))

    def test_incoming_data_json_serialization(self):
        """
        Test che l'oggetto IncomingData possa essere serializzato in JSON.
        Utile per debugging e logging.
        """
        incoming = IncomingData(source='eddn', data=self.test_data)
        original_guid = incoming.guid
        
        # Converti in dict
        data_dict = asdict(incoming)
        
        # Verifica che guid sia nel dict
        self.assertIn('guid', data_dict)
        self.assertEqual(data_dict['guid'], original_guid)
        
        # Verifica che possa essere serializzato in JSON
        json_str = json.dumps(data_dict)
        self.assertIsInstance(json_str, str)
        
        # Deserializza e verifica
        reloaded_dict = json.loads(json_str)
        self.assertEqual(reloaded_dict['guid'], original_guid)
        self.assertEqual(reloaded_dict['source'], 'eddn')
        self.assertEqual(reloaded_dict['data'], self.test_data)

    def test_incoming_data_to_dict_includes_guid(self):
        """Test che il metodo to_dict() includa il guid."""
        incoming = IncomingData(source='eddn', data=self.test_data)
        
        data_dict = incoming.to_dict()
        
        self.assertIn('guid', data_dict)
        self.assertEqual(data_dict['guid'], incoming.guid)
        self.assertIn('source', data_dict)
        self.assertIn('data', data_dict)

    def test_celery_kwargs_simulation(self):
        """
        Simula come Celery passa gli argomenti ai task.
        Verifica che l'oggetto possa essere passato come kwarg e mantenere il guid.
        """
        # Crea l'oggetto come farebbe il client EDDN
        original = IncomingData(source='eddn', data=self.test_data)
        original_guid = original.guid
        
        # Simula il passaggio attraverso Celery kwargs
        kwargs = {'istance': original, 'agent': None}
        
        # Serializza (come fa Celery quando invia alla coda)
        serialized_kwargs = pickle.dumps(kwargs)
        
        # Deserializza (come fa Celery nel worker)
        deserialized_kwargs = pickle.loads(serialized_kwargs)
        
        # Verifica che l'istanza nel worker abbia il guid
        istance = deserialized_kwargs['istance']
        self.assertTrue(hasattr(istance, 'guid'))
        self.assertEqual(istance.guid, original_guid)
        
        # Verifica che possiamo accedere al guid senza AttributeError
        try:
            guid_value = istance.guid
            self.assertEqual(guid_value, original_guid)
        except AttributeError as e:
            self.fail(f"AttributeError when accessing guid: {e}")

    def test_incoming_data_str_representation(self):
        """Test che __str__ restituisca il guid."""
        incoming = IncomingData(source='eddn', data=self.test_data)
        
        str_repr = str(incoming)
        self.assertEqual(str_repr, incoming.guid)

    def test_incoming_data_invalid_source(self):
        """Test che venga sollevata un'eccezione per sorgenti non valide."""
        with self.assertRaises(ValueError) as context:
            IncomingData(source='invalid_source', data=self.test_data)
        
        self.assertIn('Invalid source', str(context.exception))

    def test_incoming_data_valid_sources(self):
        """Test che le sorgenti valide funzionino correttamente."""
        # Test eddn
        eddn_incoming = IncomingData(source='eddn', data=self.test_data)
        self.assertEqual(eddn_incoming.source, 'eddn')
        self.assertTrue(hasattr(eddn_incoming, 'guid'))
        
        # Test capi_api
        capi_incoming = IncomingData(source='capi_api', data=self.test_data)
        self.assertEqual(capi_incoming.source, 'capi_api')
        self.assertTrue(hasattr(capi_incoming, 'guid'))

    def test_incoming_data_frozen(self):
        """Test che la dataclass sia frozen (immutabile)."""
        incoming = IncomingData(source='eddn', data=self.test_data)
        
        # Tentare di modificare un attributo dovrebbe sollevare un'eccezione
        with self.assertRaises(Exception):  # FrozenInstanceError o AttributeError
            incoming.source = 'capi_api'

    def test_guid_explicit_value(self):
        """Test che sia possibile fornire un guid esplicito."""
        custom_guid = "custom-test-guid-12345"
        incoming = IncomingData(
            guid=custom_guid,
            source='eddn',
            data=self.test_data
        )
        
        self.assertEqual(incoming.guid, custom_guid)
        
        # Verifica che possa essere serializzato/deserializzato
        serialized = pickle.dumps(incoming)
        deserialized = pickle.loads(serialized)
        
        self.assertEqual(deserialized.guid, custom_guid)
