from django.test import TestCase


from ed_dbsync.analysts import (
    JournalAnalyst, Commodity3Analyst
)

from ed_dbsync.dataclass import IncomingData
from users.models import User

EDDN_HEADER = {
    "gamebuild": "r308767/r0 ",
    "uploaderID": "78c015c631c68ceabe51f480c7e47001adae3001",
    "gameversion": "4.0.0.1904",
    "softwareName": "E:D Market Connector [Windows]",
    "softwareVersion": "5.12.1",
    "gatewayTimestamp": "2025-02-14T16:23:04.451693Z"
}

FSDJUMP_MESSAGE = {
    "Body": "Pyramio SP-M b27-9",
    "event": "CarrierJump",
    "BodyID": 0,
    "Docked": True,
    "OnFoot": True,
    "StarPos": [
        -64.3125,
        -49.59375,
        5925.21875
    ],
    "odyssey": True,
    "BodyType": "Star",
    "horizons": True,
    "timestamp": "2025-02-14T16:23:01Z",
    "Population": 0,
    "StarSystem": "Pyramio SP-M b27-9",
    "SystemAddress": 20461358296809,
    "SystemEconomy": "$economy_None;",
    "SystemSecurity": "$GAlAXY_MAP_INFO_state_anarchy;",
    "SystemAllegiance": "",
    "SystemGovernment": "$government_None;",
    "SystemSecondEconomy": "$economy_None;"
}

DOKED_MESSAGE = {
    "Taxi": False,
    "event": "Docked",
    "StarPos": [
        17.03125,
        -172.78125,
        -3.46875
    ],
    "odyssey": True,
    "MarketID": 3710910208,
    "horizons": True,
    "timestamp": "2025-02-11T16:54:55Z",
    "StarSystem": "Muang",
    "LandingPads": {
        "Large": 8,
        "Small": 4,
        "Medium": 4
    },
    "StationName": "V8Y-5HQ",
    "StationType": "FleetCarrier",
    "SystemAddress": 4481966019282,
    "DistFromStarLS": 176.749311,
    "StationEconomy": "$economy_Carrier;",
    "StationFaction": {
        "Name": "FleetCarrier"
    },
    "StationServices": [
        "dock",
        "autodock",
        "commodities",
        "contacts",
        "exploration",
        "crewlounge",
        "rearm",
        "refuel",
        "repair",
        "engineer",
        "flightcontroller",
        "stationoperations",
        "stationMenu",
        "carriermanagement",
        "carrierfuel",
        "voucherredemption",
        "socialspace",
        "bartender",
        "vistagenomics",
        "pioneersupplies"
    ],
    "StationEconomies": [
        {
            "Name": "$economy_Carrier;",
            "Proportion": 1.0
        }
    ],
    "StationGovernment": "$government_Carrier;"
}

COMMODITYV3_MESSAGE = {
    "odyssey": True,
    "horizons": True,
    "marketId": 3223781376,
    "economies": [
        {
            "name": "Industrial",
            "proportion": 0.77
        },
        {
            "name": "Extraction",
            "proportion": 0.23
        }
    ],
    "timestamp": "2025-02-14T23:44:30Z",
    "prohibited": [
        "Slaves"
    ],
    "systemName": "Synteini",
    "commodities": [
        {
            "name": "ReactiveArmour",
            "stock": 0,
            "demand": 1819,
            "buyPrice": 0,
            "meanPrice": 2224,
            "sellPrice": 2130,
            "stockBracket": 0,
            "demandBracket": 3
        }
    ],
    "stationName": "Chernykh Station"
}

class JournalAnalystTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.agent = User.objects.create_user(
            username='FSDJumpSerializerTestCase'
        )

    def test_get_event_CarrierJump(self):
        data = IncomingData(
            source='eddn',
            data={
                "header": EDDN_HEADER,
                "message": FSDJUMP_MESSAGE
            }
        )
        analyst = JournalAnalyst(data, self.agent)
        self.assertEqual(
            analyst.get_event(), 'CarrierJump', 
            "The event should be 'CarrierJump' based on the provided message."
        )

    def test_get_serializer_class_CarrierJump(self):
        data = IncomingData(
            source='eddn',
            data={
                "header": EDDN_HEADER,
                "message": FSDJUMP_MESSAGE
            }
        )
        analyst = JournalAnalyst(data, self.agent)
        serializer_class = analyst.get_serializer_class()
        self.assertEqual(
            serializer_class, analyst.serializer_CarrierJump(),
            "The serializer class should be CarrierJumpSerializer based on the event 'CarrierJump'."
        )

    def test_get_event_Docked(self):
        data = IncomingData(
            source='eddn',
            data={
                "header": EDDN_HEADER,
                "message": DOKED_MESSAGE
            }
        )
        analyst = JournalAnalyst(data, self.agent)
        self.assertEqual(
            analyst.get_event(), 'Docked', 
            "The event should be 'Docked' based on the provided message."
        )

    def test_get_serializer_class_Docked(self):
        data = IncomingData(
            source='eddn',
            data={
                "header": EDDN_HEADER,
                "message": DOKED_MESSAGE
            }
        )
        analyst = JournalAnalyst(data, self.agent)
        serializer_class = analyst.get_serializer_class()
        self.assertEqual(
            serializer_class, analyst.serializer_Docked(),
            "The serializer class should be DockedSerializer based on the event 'Docked'."
        )
    
class Commodity3AnalystTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.agent = User.objects.create_user(
            username='Commodity3AnalystTestCase'
        )

    def test_get_serializer(self):
        data = IncomingData(
            source='eddn',
            data={
                "header": EDDN_HEADER,
                "message": COMMODITYV3_MESSAGE
            }
        )
        analyst = Commodity3Analyst(data, self.agent)
        serializer_class = analyst.get_serializer_class()
        self.assertEqual(
            serializer_class.__name__, 'CommodityV3Serializer',
            "The serializer class should be CommodityV3Serializer."
        )