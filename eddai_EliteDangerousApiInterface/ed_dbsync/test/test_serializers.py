from django.test import TestCase

from ed_dbsync.serializers import (
    FSDJumpSerializer, DockedSerializer, LocationSerializer,
    CarrierJumpSerializer, CommodityV3Serializer
)

from users.models import User

FSD_JUMP_TEST_DATA = [
    {
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
    },
    {
        "Body": "Outorst SY-Q c18-1",
        "Taxi": False,
        "event": "CarrierJump",
        "BodyID": 0,
        "Docked": True,
        "StarPos": [
            -1901.1875,
            30.0,
            -1519.34375
        ],
        "odyssey": False,
        "BodyType": "Star",
        "MarketID": 3706539520,
        "horizons": True,
        "Multicrew": False,
        "timestamp": "2025-02-14T16:23:13Z",
        "Population": 0,
        "StarSystem": "Outorst SY-Q c18-1",
        "StationName": "M2X-T4Z",
        "StationType": "FleetCarrier",
        "SystemAddress": 355576353186,
        "SystemEconomy": "$economy_None;",
        "StationEconomy": "$economy_Carrier;",
        "StationFaction": {
            "Name": "FleetCarrier"
        },
        "SystemSecurity": "$GAlAXY_MAP_INFO_state_anarchy;",
        "StationServices": [
            "dock",
            "autodock",
            "commodities",
            "contacts",
            "crewlounge",
            "refuel",
            "repair",
            "shipyard",
            "engineer",
            "flightcontroller",
            "stationoperations",
            "stationMenu",
            "carriermanagement",
            "carrierfuel",
            "socialspace"
        ],
        "StationEconomies": [
            {
                "Name": "$economy_Carrier;",
                "Proportion": 1.0
            }
        ],
        "SystemAllegiance": "",
        "SystemGovernment": "$government_None;",
        "StationGovernment": "$government_Carrier;",
        "SystemSecondEconomy": "$economy_None;"
    },
    {
        "Body": "Duamta 2 a",
        "Taxi": False,
        "event": "CarrierJump",
        "BodyID": 9,
        "Docked": True,
        "StarPos": [
            2.1875,
            6.625,
            -7.0
        ],
        "odyssey": True,
        "BodyType": "Planet",
        "Factions": [
            {
                "Name": "Independents of Duamta",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.093093,
                "Allegiance": "Federation",
                "Government": "Democracy",
                "FactionState": "None"
            },
            {
                "Name": "Duamta Jet Power Commodities",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.103103,
                "Allegiance": "Federation",
                "Government": "Corporate",
                "FactionState": "None"
            },
            {
                "Name": "Defence Force of Duamta",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.055055,
                "Allegiance": "Independent",
                "Government": "Dictatorship",
                "FactionState": "None"
            },
            {
                "Name": "Duamta Gold Creative Corp.",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.45045,
                "Allegiance": "Federation",
                "Government": "Corporate",
                "ActiveStates": [
                    {
                        "State": "CivilLiberty"
                    }
                ],
                "FactionState": "CivilLiberty"
            },
            {
                "Name": "Bureau of Duamta Conservatives",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.06006,
                "Allegiance": "Independent",
                "Government": "Dictatorship",
                "FactionState": "None"
            },
            {
                "Name": "The Order of The Smiling Moose",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.104104,
                "Allegiance": "Federation",
                "Government": "Democracy",
                "FactionState": "None"
            },
            {
                "Name": "Aegis Core",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.01001,
                "Allegiance": "Independent",
                "Government": "Cooperative",
                "FactionState": "None"
            },
            {
                "Name": "Mars Congressional Republic Navy",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.124124,
                "Allegiance": "Federation",
                "Government": "Confederacy",
                "FactionState": "None"
            }
        ],
        "MarketID": 3707730944,
        "horizons": True,
        "Multicrew": False,
        "timestamp": "2025-02-05T13:18:11Z",
        "Population": 13327723347,
        "StarSystem": "Duamta",
        "StationName": "K3W-48G",
        "StationType": "FleetCarrier",
        "SystemAddress": 4339804408171,
        "SystemEconomy": "$economy_HighTech;",
        "SystemFaction": {
            "Name": "Duamta Gold Creative Corp.",
            "FactionState": "CivilLiberty"
        },
        "StationEconomy": "$economy_Carrier;",
        "StationFaction": {
            "Name": "FleetCarrier"
        },
        "SystemSecurity": "$SYSTEM_SECURITY_high;",
        "StationServices": [
            "dock",
            "autodock",
            "commodities",
            "contacts",
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
            "socialspace"
        ],
        "StationEconomies": [
            {
                "Name": "$economy_Carrier;",
                "Proportion": 1.0
            }
        ],
        "SystemAllegiance": "Federation",
        "SystemGovernment": "$government_Corporate;",
        "StationGovernment": "$government_Carrier;",
        "SystemSecondEconomy": "$economy_Agri;"
    }
]

DOCKED_TEST_DATA = [
    {
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
    },
    {
        "Taxi": False,
        "event": "Docked",
        "StarPos": [
            41.9375,
            74.65625,
            3.4375
        ],
        "odyssey": True,
        "MarketID": 3229370368,
        "horizons": True,
        "Multicrew": False,
        "timestamp": "2025-02-11T16:55:00Z",
        "StarSystem": "Ross 129",
        "LandingPads": {
            "Large": 9,
            "Small": 17,
            "Medium": 18
        },
        "StationName": "Yang Hub",
        "StationType": "Coriolis",
        "SystemAddress": 671491564969,
        "DistFromStarLS": 455.668714,
        "StationEconomy": "$economy_Industrial;",
        "StationFaction": {
            "Name": "Wolf 406 Transport & Co",
            "FactionState": "Expansion"
        },
        "StationServices": [
            "dock",
            "autodock",
            "commodities",
            "contacts",
            "exploration",
            "missions",
            "outfitting",
            "crewlounge",
            "rearm",
            "refuel",
            "repair",
            "shipyard",
            "tuning",
            "engineer",
            "missionsgenerated",
            "flightcontroller",
            "stationoperations",
            "powerplay",
            "searchrescue",
            "materialtrader",
            "stationMenu",
            "shop",
            "livery",
            "socialspace",
            "bartender",
            "vistagenomics",
            "pioneersupplies",
            "apexinterstellar",
            "frontlinesolutions"
        ],
        "StationEconomies": [
            {
                "Name": "$economy_Industrial;",
                "Proportion": 0.77
            },
            {
                "Name": "$economy_Extraction;",
                "Proportion": 0.23
            }
        ],
        "StationAllegiance": "Alliance",
        "StationGovernment": "$government_Corporate;"
    },
    {
        "Taxi": False,
        "event": "Docked",
        "StarPos": [
            41.9375,
            74.65625,
            3.4375
        ],
        "odyssey": True,
        "MarketID": 3229370368,
        "horizons": True,
        "Multicrew": False,
        "timestamp": "2025-02-11T18:00:00Z",
        "StarSystem": "Ross 129",
        "LandingPads": {
            "Large": 9,
            "Small": 17,
            "Medium": 18
        },
        "StationName": "Yang Hub",
        "StationType": "Coriolis",
        "SystemAddress": 671491564969,
        "DistFromStarLS": 455.668714,
        "StationEconomy": "$economy_Industrial;",
        "StationFaction": {
            "Name": "Wolf 406 Transport & Co",
            "FactionState": "Expansion"
        },
        "StationServices": [
            "dock",
            "autodock",
            "commodities",
            "contacts",
            "rearm",
            "refuel",
            "repair",
            "shipyard",
            "tuning",
            "engineer",
            "missionsgenerated",
            "flightcontroller",
            "stationoperations",
            "powerplay",
            "searchrescue",
            "materialtrader",
            "stationMenu",
            "shop",
            "livery",
            "socialspace",
            "bartender",
            "vistagenomics",
            "pioneersupplies",
            "apexinterstellar",
            "frontlinesolutions"
        ],
        "StationEconomies": [
            {
                "Name": "$economy_Industrial;",
                "Proportion": 0.77
            }
        ],
        "StationAllegiance": "Alliance",
        "StationGovernment": "$government_Corporate;"
    }
]

LOCATION_TEST_DATA = [
    {
        "Body": "HIP 80162 A 4",
        "Taxi": False,
        "event": "Location",
        "BodyID": 10,
        "Docked": True,
        "StarPos": [
            -54.96875,
            108.46875,
            139.96875
        ],
        "odyssey": True,
        "BodyType": "Planet",
        "Factions": [
            {
                "Name": "Workers of HIP 80162 Free",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.06513,
                "Allegiance": "Independent",
                "Government": "Democracy",
                "FactionState": "None"
            },
            {
                "Name": "New HIP 80162 First",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.012024,
                "Allegiance": "Independent",
                "Government": "Dictatorship",
                "FactionState": "None"
            },
            {
                "Name": "HIP 80162 State Commodities",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.093186,
                "Allegiance": "Independent",
                "Government": "Corporate",
                "FactionState": "None"
            },
            {
                "Name": "HIP 80162 Ring",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.017034,
                "Allegiance": "Independent",
                "Government": "Anarchy",
                "FactionState": "None"
            },
            {
                "Name": "Division Cassini",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.220441,
                "Allegiance": "Independent",
                "Government": "Cooperative",
                "ActiveStates": [
                    {
                        "State": "Expansion"
                    }
                ],
                "FactionState": "Expansion"
            },
            {
                "Name": "Talon Security",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.592184,
                "Allegiance": "Independent",
                "Government": "Corporate",
                "FactionState": "None"
            }
        ],
        "MarketID": 3702263296,
        "horizons": True,
        "Multicrew": False,
        "timestamp": "2025-02-13T17:00:24Z",
        "Population": 5645792,
        "StarSystem": "HIP 80162",
        "StationName": "XNF-NQF",
        "StationType": "FleetCarrier",
        "SystemAddress": 1109989017979,
        "SystemEconomy": "$economy_Industrial;",
        "SystemFaction": {
            "Name": "Talon Security"
        },
        "DistFromStarLS": 1640.185842,
        "StationEconomy": "$economy_Carrier;",
        "StationFaction": {
            "Name": "FleetCarrier"
        },
        "SystemSecurity": "$SYSTEM_SECURITY_medium;",
        "StationServices": [
            "dock",
            "autodock",
            "commodities",
            "contacts",
            "outfitting",
            "crewlounge",
            "rearm",
            "refuel",
            "repair",
            "shipyard",
            "engineer",
            "flightcontroller",
            "stationoperations",
            "stationMenu",
            "carriermanagement",
            "carrierfuel",
            "livery",
            "socialspace",
            "bartender"
        ],
        "StationEconomies": [
            {
                "Name": "$economy_Carrier;",
                "Proportion": 1.0
            }
        ],
        "SystemAllegiance": "Independent",
        "SystemGovernment": "$government_Corporate;",
        "StationGovernment": "$government_Carrier;",
        "SystemSecondEconomy": "$economy_Extraction;"
    },
    {
        "Body": "Bean Terminal",
        "Taxi": False,
        "event": "Location",
        "BodyID": 17,
        "Docked": True,
        "Powers": [
            "A. Lavigny-Duval",
            "Aisling Duval",
            "Felicia Winters",
            "Zemina Torval"
        ],
        "StarPos": [
            18.25,
            -39.09375,
            36.9375
        ],
        "odyssey": True,
        "BodyType": "Station",
        "Factions": [
            {
                "Name": "Progressive Party of Anekaliti",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.012048,
                "Allegiance": "Federation",
                "Government": "Democracy",
                "FactionState": "None",
                "RecoveringStates": [
                    {
                        "State": "Outbreak",
                        "Trend": 0
                    }
                ]
            },
            {
                "Name": "Anekaliti Dragons",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.01004,
                "Allegiance": "Independent",
                "Government": "Anarchy",
                "FactionState": "None",
                "RecoveringStates": [
                    {
                        "State": "NaturalDisaster",
                        "Trend": 0
                    }
                ]
            },
            {
                "Name": "Silver Legal Ltd",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.059237,
                "Allegiance": "Federation",
                "Government": "Corporate",
                "FactionState": "None"
            },
            {
                "Name": "Anekaliti Purple Comms Co",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.103414,
                "Allegiance": "Federation",
                "Government": "Corporate",
                "FactionState": "None"
            },
            {
                "Name": "Justice Party of Anekaliti",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.017068,
                "Allegiance": "Independent",
                "Government": "Dictatorship",
                "FactionState": "None"
            },
            {
                "Name": "L 119-33 United Co",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.672691,
                "Allegiance": "Federation",
                "Government": "Corporate",
                "ActiveStates": [
                    {
                        "State": "Boom"
                    }
                ],
                "FactionState": "Boom"
            },
            {
                "Name": "Paladin Consortium",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.125502,
                "Allegiance": "Independent",
                "Government": "Democracy",
                "ActiveStates": [
                    {
                        "State": "Expansion"
                    }
                ],
                "FactionState": "Expansion"
            }
        ],
        "MarketID": 3223921920,
        "horizons": True,
        "Multicrew": False,
        "timestamp": "2025-02-13T17:00:30Z",
        "Population": 2316834,
        "StarSystem": "Anekaliti",
        "StationName": "Bean Terminal",
        "StationType": "Bernal",
        "SystemAddress": 5369245748080,
        "SystemEconomy": "$economy_Industrial;",
        "SystemFaction": {
            "Name": "L 119-33 United Co",
            "FactionState": "Boom"
        },
        "DistFromStarLS": 789.624074,
        "PowerplayState": "Exploited",
        "StationEconomy": "$economy_Industrial;",
        "StationFaction": {
            "Name": "L 119-33 United Co",
            "FactionState": "Boom"
        },
        "SystemSecurity": "$SYSTEM_SECURITY_medium;",
        "StationServices": [
            "dock",
            "autodock",
            "commodities",
            "contacts",
            "exploration",
            "missions",
            "outfitting",
            "crewlounge",
            "rearm",
            "refuel",
            "repair",
            "shipyard",
            "tuning",
            "engineer",
            "missionsgenerated",
            "flightcontroller",
            "stationoperations",
            "powerplay",
            "searchrescue",
            "stationMenu",
            "shop",
            "livery",
            "socialspace",
            "bartender",
            "vistagenomics",
            "pioneersupplies",
            "apexinterstellar",
            "frontlinesolutions"
        ],
        "ControllingPower": "Zemina Torval",
        "StationEconomies": [
            {
                "Name": "$economy_Industrial;",
                "Proportion": 1.0
            }
        ],
        "SystemAllegiance": "Federation",
        "SystemGovernment": "$government_Corporate;",
        "StationAllegiance": "Federation",
        "StationGovernment": "$government_Corporate;",
        "SystemSecondEconomy": "$economy_None;"
    },
    {
        "Body": "Sterope II A",
        "Taxi": False,
        "event": "Location",
        "BodyID": 1,
        "Docked": True,
        "StarPos": [
            -81.65625,
            -147.28125,
            -340.84375
        ],
        "odyssey": True,
        "BodyType": "Star",
        "MarketID": 3704117248,
        "horizons": True,
        "Multicrew": False,
        "timestamp": "2025-02-13T17:00:30Z",
        "Population": 0,
        "StarSystem": "Sterope II",
        "StationName": "T9Q-32F",
        "StationType": "FleetCarrier",
        "SystemAddress": 220349850788,
        "SystemEconomy": "$economy_None;",
        "StationEconomy": "$economy_Carrier;",
        "StationFaction": {
            "Name": "FleetCarrier"
        },
        "SystemSecurity": "$GAlAXY_MAP_INFO_state_anarchy;",
        "StationServices": [
            "dock",
            "autodock",
            "commodities",
            "contacts",
            "outfitting",
            "crewlounge",
            "rearm",
            "refuel",
            "repair",
            "shipyard",
            "engineer",
            "flightcontroller",
            "stationoperations",
            "stationMenu",
            "carriermanagement",
            "carrierfuel",
            "livery",
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
        "SystemAllegiance": "",
        "SystemGovernment": "$government_None;",
        "StationGovernment": "$government_Carrier;",
        "SystemSecondEconomy": "$economy_None;"
    },
    {
        "Body": "Borrego Station",
        "Taxi": False,
        "event": "Location",
        "BodyID": 47,
        "Docked": True,
        "StarPos": [
            66.8125,
            -210.625,
            -36.875
        ],
        "odyssey": True,
        "BodyType": "Station",
        "Factions": [
            {
                "Name": "HIP 10483 Justice Party",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.061265,
                "Allegiance": "Empire",
                "Government": "Dictatorship",
                "FactionState": "None"
            },
            {
                "Name": "Menero Kimi Empire Group",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.131423,
                "Allegiance": "Empire",
                "Government": "Patronage",
                "FactionState": "None"
            },
            {
                "Name": "HIP 10483 Gold Netcoms Partners",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.020751,
                "Allegiance": "Independent",
                "Government": "Corporate",
                "FactionState": "None"
            },
            {
                "Name": "HIP 10483 Jet Camorra",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.019763,
                "Allegiance": "Independent",
                "Government": "Anarchy",
                "FactionState": "None"
            },
            {
                "Name": "Green Party of HIP 10483",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.041502,
                "Allegiance": "Independent",
                "Government": "Democracy",
                "FactionState": "None"
            },
            {
                "Name": "Coalition of the Willing",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.19664,
                "Allegiance": "Independent",
                "Government": "Democracy",
                "FactionState": "None"
            },
            {
                "Name": "LOST BOYS",
                "Happiness": "$Faction_HappinessBand2;",
                "Influence": 0.528656,
                "Allegiance": "Independent",
                "Government": "Democracy",
                "FactionState": "None"
            }
        ],
        "MarketID": 3222062080,
        "horizons": True,
        "Multicrew": False,
        "timestamp": "2025-02-13T17:00:33Z",
        "Population": 5755262,
        "StarSystem": "HIP 10483",
        "StationName": "Borrego Station",
        "StationType": "Bernal",
        "SystemAddress": 628969392483,
        "SystemEconomy": "$economy_Industrial;",
        "SystemFaction": {
            "Name": "LOST BOYS"
        },
        "DistFromStarLS": 1037.757174,
        "StationEconomy": "$economy_Industrial;",
        "StationFaction": {
            "Name": "LOST BOYS"
        },
        "SystemSecurity": "$SYSTEM_SECURITY_high;",
        "StationServices": [
            "dock",
            "autodock",
            "blackmarket",
            "commodities",
            "contacts",
            "exploration",
            "missions",
            "outfitting",
            "crewlounge",
            "rearm",
            "refuel",
            "repair",
            "shipyard",
            "tuning",
            "engineer",
            "missionsgenerated",
            "flightcontroller",
            "stationoperations",
            "powerplay",
            "searchrescue",
            "stationMenu",
            "shop",
            "livery",
            "socialspace",
            "bartender",
            "vistagenomics",
            "pioneersupplies",
            "apexinterstellar",
            "frontlinesolutions"
        ],
        "StationEconomies": [
            {
                "Name": "$economy_Industrial;",
                "Proportion": 1.0
            }
        ],
        "SystemAllegiance": "Independent",
        "SystemGovernment": "$government_Democracy;",
        "StationGovernment": "$government_Democracy;",
        "SystemSecondEconomy": "$economy_Military;"
    },
    {
        "Body": "Byua Ain GA-P c19-1250 C 2",
        "Taxi": False,
        "event": "Location",
        "BodyID": 6,
        "Docked": False,
        "StarPos": [
            -287.5625,
            4.21875,
            16421.53125
        ],
        "odyssey": True,
        "BodyType": "Planet",
        "horizons": True,
        "Multicrew": False,
        "timestamp": "2025-02-13T17:00:38Z",
        "Population": 0,
        "StarSystem": "Byua Ain GA-P c19-1250",
        "SystemAddress": 343680766451626,
        "SystemEconomy": "$economy_None;",
        "DistFromStarLS": 6322.329736,
        "SystemSecurity": "$GAlAXY_MAP_INFO_state_anarchy;",
        "SystemAllegiance": "",
        "SystemGovernment": "$government_None;",
        "SystemSecondEconomy": "$economy_None;"
    },
    {
        "Body": "HIP 12099 1 b",
        "event": "Location",
        "BodyID": 16,
        "Docked": False,
        "StarPos": [
            -101.90625,
            -95.46875,
            -165.59375
        ],
        "odyssey": True,
        "BodyType": "Planet",
        "horizons": True,
        "timestamp": "2025-02-13T17:00:31Z",
        "Population": 0,
        "StarSystem": "HIP 12099",
        "SystemAddress": 560216394075,
        "SystemEconomy": "$economy_None;",
        "DistFromStarLS": 1101.68808,
        "SystemSecurity": "$GAlAXY_MAP_INFO_state_anarchy;",
        "SystemAllegiance": "",
        "SystemGovernment": "$government_None;",
        "SystemSecondEconomy": "$economy_None;"
    }
]

COMMODITY_V3_TEST_DATA = [
    {
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
                "name": "AgronomicTreatment",
                "stock": 0,
                "demand": 172,
                "buyPrice": 0,
                "meanPrice": 3105,
                "sellPrice": 900,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Explosives",
                "stock": 0,
                "demand": 22401,
                "buyPrice": 0,
                "meanPrice": 513,
                "sellPrice": 653,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "HydrogenFuel",
                "stock": 14514,
                "demand": 1,
                "buyPrice": 118,
                "meanPrice": 113,
                "sellPrice": 112,
                "stockBracket": 1,
                "demandBracket": 0
            },
            {
                "name": "HydrogenPeroxide",
                "stock": 0,
                "demand": 86866,
                "buyPrice": 0,
                "meanPrice": 3161,
                "sellPrice": 1783,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "LiquidOxygen",
                "stock": 0,
                "demand": 3680934,
                "buyPrice": 0,
                "meanPrice": 1473,
                "sellPrice": 3991,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Tritium",
                "stock": 0,
                "demand": 11394,
                "buyPrice": 0,
                "meanPrice": 51707,
                "sellPrice": 54776,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Water",
                "stock": 0,
                "demand": 28724,
                "buyPrice": 0,
                "meanPrice": 279,
                "sellPrice": 626,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Clothing",
                "stock": 8376,
                "demand": 1,
                "buyPrice": 206,
                "meanPrice": 546,
                "sellPrice": 186,
                "stockBracket": 2,
                "demandBracket": 0
            },
            {
                "name": "ConsumerTechnology",
                "stock": 0,
                "demand": 1577,
                "buyPrice": 0,
                "meanPrice": 6691,
                "sellPrice": 7181,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "DomesticAppliances",
                "stock": 0,
                "demand": 2473,
                "buyPrice": 0,
                "meanPrice": 740,
                "sellPrice": 877,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "SurvivalEquipment",
                "stock": 313,
                "demand": 1,
                "buyPrice": 1926,
                "meanPrice": 684,
                "sellPrice": 1794,
                "stockBracket": 1,
                "demandBracket": 0
            },
            {
                "name": "CMMComposite",
                "stock": 0,
                "demand": 8282,
                "buyPrice": 0,
                "meanPrice": 5987,
                "sellPrice": 6299,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "CeramicComposites",
                "stock": 0,
                "demand": 395703,
                "buyPrice": 0,
                "meanPrice": 415,
                "sellPrice": 1740,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "CoolingHoses",
                "stock": 0,
                "demand": 28159,
                "buyPrice": 0,
                "meanPrice": 1886,
                "sellPrice": 1848,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "InsulatingMembrane",
                "stock": 0,
                "demand": 5153,
                "buyPrice": 0,
                "meanPrice": 10724,
                "sellPrice": 11409,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Polymers",
                "stock": 0,
                "demand": 596199,
                "buyPrice": 0,
                "meanPrice": 376,
                "sellPrice": 1032,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Semiconductors",
                "stock": 0,
                "demand": 80689,
                "buyPrice": 0,
                "meanPrice": 1136,
                "sellPrice": 781,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Superconductors",
                "stock": 0,
                "demand": 55017,
                "buyPrice": 0,
                "meanPrice": 6678,
                "sellPrice": 7253,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "AtmosphericExtractors",
                "stock": 7126,
                "demand": 1,
                "buyPrice": 356,
                "meanPrice": 571,
                "sellPrice": 330,
                "stockBracket": 2,
                "demandBracket": 0
            },
            {
                "name": "BuildingFabricators",
                "stock": 144,
                "demand": 1,
                "buyPrice": 1944,
                "meanPrice": 2311,
                "sellPrice": 1884,
                "stockBracket": 1,
                "demandBracket": 0
            },
            {
                "name": "CropHarvesters",
                "stock": 5048,
                "demand": 1,
                "buyPrice": 1655,
                "meanPrice": 2230,
                "sellPrice": 1603,
                "stockBracket": 2,
                "demandBracket": 0
            },
            {
                "name": "EmergencyPowerCells",
                "stock": 0,
                "demand": 4419,
                "buyPrice": 0,
                "meanPrice": 2368,
                "sellPrice": 2272,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "GeologicalEquipment",
                "stock": 14635,
                "demand": 1,
                "buyPrice": 1566,
                "meanPrice": 1886,
                "sellPrice": 1516,
                "stockBracket": 1,
                "demandBracket": 0
            },
            {
                "name": "HNShockMount",
                "stock": 5792,
                "demand": 1,
                "buyPrice": 1681,
                "meanPrice": 1923,
                "sellPrice": 1628,
                "stockBracket": 2,
                "demandBracket": 0
            },
            {
                "name": "MarineSupplies",
                "stock": 30367,
                "demand": 1,
                "buyPrice": 3568,
                "meanPrice": 4136,
                "sellPrice": 3463,
                "stockBracket": 2,
                "demandBracket": 0
            },
            {
                "name": "MineralExtractors",
                "stock": 15904,
                "demand": 1,
                "buyPrice": 630,
                "meanPrice": 801,
                "sellPrice": 598,
                "stockBracket": 2,
                "demandBracket": 0
            },
            {
                "name": "PowerGenerators",
                "stock": 5977,
                "demand": 1,
                "buyPrice": 2549,
                "meanPrice": 2466,
                "sellPrice": 2471,
                "stockBracket": 1,
                "demandBracket": 0
            },
            {
                "name": "SkimerComponents",
                "stock": 599,
                "demand": 1,
                "buyPrice": 515,
                "meanPrice": 1119,
                "sellPrice": 491,
                "stockBracket": 2,
                "demandBracket": 0
            },
            {
                "name": "ThermalCoolingUnits",
                "stock": 127,
                "demand": 1,
                "buyPrice": 3847,
                "meanPrice": 3761,
                "sellPrice": 3732,
                "stockBracket": 1,
                "demandBracket": 0
            },
            {
                "name": "WaterPurifiers",
                "stock": 1284,
                "demand": 1,
                "buyPrice": 1669,
                "meanPrice": 484,
                "sellPrice": 1503,
                "stockBracket": 1,
                "demandBracket": 0
            },
            {
                "name": "AdvancedMedicines",
                "stock": 0,
                "demand": 4884036,
                "buyPrice": 0,
                "meanPrice": 1485,
                "sellPrice": 3302,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "BasicMedicines",
                "stock": 4703,
                "demand": 1,
                "buyPrice": 2856,
                "meanPrice": 493,
                "sellPrice": 2577,
                "stockBracket": 1,
                "demandBracket": 0
            },
            {
                "name": "CombatStabilisers",
                "stock": 0,
                "demand": 271,
                "buyPrice": 0,
                "meanPrice": 3652,
                "sellPrice": 2819,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "OnionHeadC",
                "stock": 0,
                "demand": 4053,
                "buyPrice": 0,
                "meanPrice": 4828,
                "sellPrice": 613,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "PerformanceEnhancers",
                "stock": 0,
                "demand": 1825,
                "buyPrice": 0,
                "meanPrice": 6790,
                "sellPrice": 7181,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "ProgenitorCells",
                "stock": 0,
                "demand": 509,
                "buyPrice": 0,
                "meanPrice": 6751,
                "sellPrice": 7181,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Aluminium",
                "stock": 0,
                "demand": 152752,
                "buyPrice": 0,
                "meanPrice": 551,
                "sellPrice": 580,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Beryllium",
                "stock": 0,
                "demand": 42514,
                "buyPrice": 0,
                "meanPrice": 8242,
                "sellPrice": 8717,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Cobalt",
                "stock": 19668,
                "demand": 1,
                "buyPrice": 1537,
                "meanPrice": 3761,
                "sellPrice": 1460,
                "stockBracket": 1,
                "demandBracket": 0
            },
            {
                "name": "Copper",
                "stock": 0,
                "demand": 213484,
                "buyPrice": 0,
                "meanPrice": 689,
                "sellPrice": 862,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Gallium",
                "stock": 0,
                "demand": 30368,
                "buyPrice": 0,
                "meanPrice": 5202,
                "sellPrice": 5473,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Gold",
                "stock": 0,
                "demand": 6150,
                "buyPrice": 0,
                "meanPrice": 47609,
                "sellPrice": 49588,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Indium",
                "stock": 0,
                "demand": 13804,
                "buyPrice": 0,
                "meanPrice": 5844,
                "sellPrice": 6299,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Lithium",
                "stock": 0,
                "demand": 153119,
                "buyPrice": 0,
                "meanPrice": 1771,
                "sellPrice": 1604,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Osmium",
                "stock": 0,
                "demand": 25397,
                "buyPrice": 0,
                "meanPrice": 45210,
                "sellPrice": 45739,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Palladium",
                "stock": 0,
                "demand": 29724,
                "buyPrice": 0,
                "meanPrice": 50639,
                "sellPrice": 52847,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Platinum",
                "stock": 0,
                "demand": 7888,
                "buyPrice": 0,
                "meanPrice": 58272,
                "sellPrice": 56070,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Praseodymium",
                "stock": 0,
                "demand": 22268,
                "buyPrice": 0,
                "meanPrice": 8620,
                "sellPrice": 8198,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Samarium",
                "stock": 0,
                "demand": 14171,
                "buyPrice": 0,
                "meanPrice": 25853,
                "sellPrice": 14490,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Silver",
                "stock": 0,
                "demand": 10396,
                "buyPrice": 0,
                "meanPrice": 37223,
                "sellPrice": 36854,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Tantalum",
                "stock": 0,
                "demand": 18588,
                "buyPrice": 0,
                "meanPrice": 4043,
                "sellPrice": 4235,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Titanium",
                "stock": 0,
                "demand": 54845,
                "buyPrice": 0,
                "meanPrice": 1208,
                "sellPrice": 897,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Uranium",
                "stock": 0,
                "demand": 121835,
                "buyPrice": 0,
                "meanPrice": 2826,
                "sellPrice": 2827,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Bauxite",
                "stock": 5914,
                "demand": 1,
                "buyPrice": 2678,
                "meanPrice": 1140,
                "sellPrice": 2549,
                "statusFlags": [
                    "powerplay"
                ],
                "stockBracket": 2,
                "demandBracket": 0
            },
            {
                "name": "Bertrandite",
                "stock": 1036,
                "demand": 1,
                "buyPrice": 13000,
                "meanPrice": 18817,
                "sellPrice": 12601,
                "statusFlags": [
                    "powerplay"
                ],
                "stockBracket": 2,
                "demandBracket": 0
            },
            {
                "name": "Coltan",
                "stock": 2168,
                "demand": 1,
                "buyPrice": 3340,
                "meanPrice": 6163,
                "sellPrice": 3187,
                "statusFlags": [
                    "powerplay"
                ],
                "stockBracket": 2,
                "demandBracket": 0
            },
            {
                "name": "Gallite",
                "stock": 1296,
                "demand": 1,
                "buyPrice": 8307,
                "meanPrice": 11915,
                "sellPrice": 8055,
                "statusFlags": [
                    "powerplay"
                ],
                "stockBracket": 2,
                "demandBracket": 0
            },
            {
                "name": "Indite",
                "stock": 1508,
                "demand": 1,
                "buyPrice": 7468,
                "meanPrice": 11389,
                "sellPrice": 7236,
                "statusFlags": [
                    "powerplay"
                ],
                "stockBracket": 2,
                "demandBracket": 0
            },
            {
                "name": "Lepidolite",
                "stock": 448,
                "demand": 1,
                "buyPrice": 1706,
                "meanPrice": 772,
                "sellPrice": 1618,
                "statusFlags": [
                    "powerplay"
                ],
                "stockBracket": 2,
                "demandBracket": 0
            },
            {
                "name": "LowTemperatureDiamond",
                "stock": 0,
                "demand": 0,
                "buyPrice": 0,
                "meanPrice": 106382,
                "sellPrice": 23872,
                "statusFlags": [
                    "powerplay"
                ],
                "stockBracket": 0,
                "demandBracket": 1
            },
            {
                "name": "Painite",
                "stock": 0,
                "demand": 1250,
                "buyPrice": 0,
                "meanPrice": 53032,
                "sellPrice": 27146,
                "statusFlags": [
                    "powerplay"
                ],
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Rutile",
                "stock": 1673,
                "demand": 1,
                "buyPrice": 3288,
                "meanPrice": 2083,
                "sellPrice": 3185,
                "statusFlags": [
                    "powerplay"
                ],
                "stockBracket": 2,
                "demandBracket": 0
            },
            {
                "name": "Uraninite",
                "stock": 15550,
                "demand": 1,
                "buyPrice": 1104,
                "meanPrice": 2958,
                "sellPrice": 1051,
                "statusFlags": [
                    "powerplay"
                ],
                "stockBracket": 2,
                "demandBracket": 0
            },
            {
                "name": "BasicNarcotics",
                "stock": 0,
                "demand": 10108,
                "buyPrice": 0,
                "meanPrice": 10124,
                "sellPrice": 10487,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Beer",
                "stock": 0,
                "demand": 34463,
                "buyPrice": 0,
                "meanPrice": 430,
                "sellPrice": 360,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "BootlegLiquor",
                "stock": 0,
                "demand": 6289,
                "buyPrice": 0,
                "meanPrice": 779,
                "sellPrice": 725,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Liquor",
                "stock": 0,
                "demand": 12622,
                "buyPrice": 0,
                "meanPrice": 879,
                "sellPrice": 1438,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Tobacco",
                "stock": 0,
                "demand": 3344,
                "buyPrice": 0,
                "meanPrice": 5324,
                "sellPrice": 5613,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Wine",
                "stock": 0,
                "demand": 11993,
                "buyPrice": 0,
                "meanPrice": 507,
                "sellPrice": 690,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "DamagedEscapePod",
                "stock": 0,
                "demand": 872,
                "buyPrice": 0,
                "meanPrice": 16966,
                "sellPrice": 8595,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Hostage",
                "stock": 0,
                "demand": 215,
                "buyPrice": 0,
                "meanPrice": 34605,
                "sellPrice": 35161,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "OccupiedCryoPod",
                "stock": 0,
                "demand": 215,
                "buyPrice": 0,
                "meanPrice": 30364,
                "sellPrice": 15113,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "PersonalEffects",
                "stock": 0,
                "demand": 215,
                "buyPrice": 0,
                "meanPrice": 9544,
                "sellPrice": 9463,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "ThargoidPod",
                "stock": 0,
                "demand": 700,
                "buyPrice": 0,
                "meanPrice": 148147,
                "sellPrice": 149851,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "ThargoidTissueSampleType6",
                "stock": 0,
                "demand": 700,
                "buyPrice": 0,
                "meanPrice": 70981,
                "sellPrice": 72153,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "ThargoidTissueSampleType9a",
                "stock": 0,
                "demand": 700,
                "buyPrice": 0,
                "meanPrice": 496635,
                "sellPrice": 499880,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "ThargoidTissueSampleType9b",
                "stock": 0,
                "demand": 700,
                "buyPrice": 0,
                "meanPrice": 271074,
                "sellPrice": 273418,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "ThargoidTissueSampleType9c",
                "stock": 0,
                "demand": 700,
                "buyPrice": 0,
                "meanPrice": 138542,
                "sellPrice": 140188,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "USSCargoBlackBox",
                "stock": 0,
                "demand": 215,
                "buyPrice": 0,
                "meanPrice": 31063,
                "sellPrice": 30904,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "UnocuppiedEscapePod",
                "stock": 0,
                "demand": 700,
                "buyPrice": 0,
                "meanPrice": 3900,
                "sellPrice": 4254,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "WreckageComponents",
                "stock": 0,
                "demand": 2135,
                "buyPrice": 0,
                "meanPrice": 9034,
                "sellPrice": 9176,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "ImperialSlaves",
                "stock": 2733,
                "demand": 1,
                "buyPrice": 17379,
                "meanPrice": 17493,
                "sellPrice": 17099,
                "stockBracket": 1,
                "demandBracket": 0
            },
            {
                "name": "AutoFabricators",
                "stock": 0,
                "demand": 7915,
                "buyPrice": 0,
                "meanPrice": 3826,
                "sellPrice": 3916,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "BioReducingLichen",
                "stock": 0,
                "demand": 34469,
                "buyPrice": 0,
                "meanPrice": 1204,
                "sellPrice": 796,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "ComputerComponents",
                "stock": 334,
                "demand": 1,
                "buyPrice": 552,
                "meanPrice": 775,
                "sellPrice": 514,
                "stockBracket": 2,
                "demandBracket": 0
            },
            {
                "name": "HazardousEnvironmentSuits",
                "stock": 0,
                "demand": 1869507,
                "buyPrice": 0,
                "meanPrice": 570,
                "sellPrice": 2053,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "MicroControllers",
                "stock": 0,
                "demand": 2945,
                "buyPrice": 0,
                "meanPrice": 5590,
                "sellPrice": 5871,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Robotics",
                "stock": 0,
                "demand": 35340,
                "buyPrice": 0,
                "meanPrice": 2019,
                "sellPrice": 1944,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "ConductiveFabrics",
                "stock": 0,
                "demand": 189092,
                "buyPrice": 0,
                "meanPrice": 709,
                "sellPrice": 1113,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "SyntheticFabrics",
                "stock": 0,
                "demand": 555043,
                "buyPrice": 0,
                "meanPrice": 416,
                "sellPrice": 763,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "Biowaste",
                "stock": 2017,
                "demand": 1,
                "buyPrice": 52,
                "meanPrice": 358,
                "sellPrice": 31,
                "stockBracket": 2,
                "demandBracket": 0
            },
            {
                "name": "Scrap",
                "stock": 17369,
                "demand": 1,
                "buyPrice": 139,
                "meanPrice": 300,
                "sellPrice": 115,
                "stockBracket": 2,
                "demandBracket": 0
            },
            {
                "name": "BattleWeapons",
                "stock": 80,
                "demand": 1,
                "buyPrice": 6050,
                "meanPrice": 7441,
                "sellPrice": 5946,
                "stockBracket": 2,
                "demandBracket": 0
            },
            {
                "name": "NonLethalWeapons",
                "stock": 0,
                "demand": 29056,
                "buyPrice": 0,
                "meanPrice": 1943,
                "sellPrice": 2576,
                "stockBracket": 0,
                "demandBracket": 3
            },
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
    },
    {
        "odyssey": True,
        "horizons": False,
        "marketId": 3871843328,
        "economies": [
            {
                "name": "Extraction",
                "proportion": 1
            }
        ],
        "timestamp": "2025-02-14T23:44:45Z",
        "prohibited": [
            "BasicNarcotics",
            "CombatStabilisers",
            "ImperialSlaves",
            "Slaves"
        ],
        "systemName": "Rhea",
        "commodities": [
            {
                "name": "advancedmedicines",
                "stock": 0,
                "demand": 104,
                "buyPrice": 0,
                "meanPrice": 1485,
                "sellPrice": 1639,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "agronomictreatment",
                "stock": 0,
                "demand": 2,
                "buyPrice": 0,
                "meanPrice": 3105,
                "sellPrice": 3598,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "animalmeat",
                "stock": 0,
                "demand": 94,
                "buyPrice": 0,
                "meanPrice": 1539,
                "sellPrice": 1803,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "basicmedicines",
                "stock": 0,
                "demand": 9,
                "buyPrice": 0,
                "meanPrice": 493,
                "sellPrice": 485,
                "stockBracket": 0,
                "demandBracket": 1
            },
            {
                "name": "beer",
                "stock": 0,
                "demand": 185,
                "buyPrice": 0,
                "meanPrice": 430,
                "sellPrice": 225,
                "stockBracket": 0,
                "demandBracket": 1
            },
            {
                "name": "bertrandite",
                "stock": 670,
                "demand": 1,
                "buyPrice": 14666,
                "meanPrice": 18817,
                "sellPrice": 14665,
                "stockBracket": 3,
                "demandBracket": 0
            },
            {
                "name": "bioreducinglichen",
                "stock": 0,
                "demand": 2412,
                "buyPrice": 0,
                "meanPrice": 1204,
                "sellPrice": 1593,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "bootlegliquor",
                "stock": 0,
                "demand": 7,
                "buyPrice": 0,
                "meanPrice": 779,
                "sellPrice": 562,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "centaurimegagin",
                "stock": 0,
                "demand": 0,
                "buyPrice": 2633,
                "meanPrice": 10217,
                "sellPrice": 20379,
                "stockBracket": 0,
                "demandBracket": 0
            },
            {
                "name": "clothing",
                "stock": 0,
                "demand": 337,
                "buyPrice": 0,
                "meanPrice": 546,
                "sellPrice": 736,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "coffee",
                "stock": 0,
                "demand": 24,
                "buyPrice": 0,
                "meanPrice": 1498,
                "sellPrice": 1803,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "coltan",
                "stock": 1080,
                "demand": 1,
                "buyPrice": 4682,
                "meanPrice": 6163,
                "sellPrice": 4681,
                "stockBracket": 2,
                "demandBracket": 0
            },
            {
                "name": "consumertechnology",
                "stock": 0,
                "demand": 16,
                "buyPrice": 0,
                "meanPrice": 6691,
                "sellPrice": 6885,
                "stockBracket": 0,
                "demandBracket": 1
            },
            {
                "name": "damagedescapepod",
                "stock": 0,
                "demand": 2,
                "buyPrice": 0,
                "meanPrice": 16966,
                "sellPrice": 16815,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "domesticappliances",
                "stock": 0,
                "demand": 101,
                "buyPrice": 0,
                "meanPrice": 740,
                "sellPrice": 972,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "explosives",
                "stock": 0,
                "demand": 708,
                "buyPrice": 0,
                "meanPrice": 513,
                "sellPrice": 859,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "fish",
                "stock": 0,
                "demand": 261,
                "buyPrice": 0,
                "meanPrice": 649,
                "sellPrice": 834,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "foodcartridges",
                "stock": 0,
                "demand": 18,
                "buyPrice": 0,
                "meanPrice": 266,
                "sellPrice": 553,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "fruitandvegetables",
                "stock": 0,
                "demand": 29,
                "buyPrice": 0,
                "meanPrice": 509,
                "sellPrice": 484,
                "stockBracket": 0,
                "demandBracket": 1
            },
            {
                "name": "grain",
                "stock": 0,
                "demand": 187,
                "buyPrice": 0,
                "meanPrice": 411,
                "sellPrice": 257,
                "stockBracket": 0,
                "demandBracket": 1
            },
            {
                "name": "hazardousenvironmentsuits",
                "stock": 0,
                "demand": 1570,
                "buyPrice": 0,
                "meanPrice": 570,
                "sellPrice": 830,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "hostage",
                "stock": 0,
                "demand": 2,
                "buyPrice": 0,
                "meanPrice": 34605,
                "sellPrice": 34477,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "hydrogenfuel",
                "stock": 0,
                "demand": 193,
                "buyPrice": 0,
                "meanPrice": 113,
                "sellPrice": 155,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "liquor",
                "stock": 0,
                "demand": 33,
                "buyPrice": 0,
                "meanPrice": 879,
                "sellPrice": 1080,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "mineralextractors",
                "stock": 0,
                "demand": 3636,
                "buyPrice": 0,
                "meanPrice": 801,
                "sellPrice": 1191,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "nonlethalweapons",
                "stock": 0,
                "demand": 3,
                "buyPrice": 0,
                "meanPrice": 1943,
                "sellPrice": 1984,
                "stockBracket": 0,
                "demandBracket": 1
            },
            {
                "name": "occupiedcryopod",
                "stock": 0,
                "demand": 2,
                "buyPrice": 0,
                "meanPrice": 30364,
                "sellPrice": 30230,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "onionheadc",
                "stock": 0,
                "demand": 84,
                "buyPrice": 0,
                "meanPrice": 4828,
                "sellPrice": 5430,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "performanceenhancers",
                "stock": 0,
                "demand": 100,
                "buyPrice": 0,
                "meanPrice": 6790,
                "sellPrice": 7373,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "personaleffects",
                "stock": 0,
                "demand": 2,
                "buyPrice": 0,
                "meanPrice": 9544,
                "sellPrice": 9466,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "personalweapons",
                "stock": 0,
                "demand": 7,
                "buyPrice": 0,
                "meanPrice": 4735,
                "sellPrice": 4421,
                "stockBracket": 0,
                "demandBracket": 1
            },
            {
                "name": "powergenerators",
                "stock": 0,
                "demand": 47,
                "buyPrice": 0,
                "meanPrice": 2466,
                "sellPrice": 2874,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "reactivearmour",
                "stock": 0,
                "demand": 8,
                "buyPrice": 0,
                "meanPrice": 2224,
                "sellPrice": 2238,
                "stockBracket": 0,
                "demandBracket": 1
            },
            {
                "name": "rutile",
                "stock": 413,
                "demand": 1,
                "buyPrice": 1584,
                "meanPrice": 2083,
                "sellPrice": 1583,
                "stockBracket": 2,
                "demandBracket": 0
            },
            {
                "name": "syntheticmeat",
                "stock": 0,
                "demand": 19,
                "buyPrice": 0,
                "meanPrice": 440,
                "sellPrice": 420,
                "stockBracket": 0,
                "demandBracket": 1
            },
            {
                "name": "tea",
                "stock": 0,
                "demand": 85,
                "buyPrice": 0,
                "meanPrice": 1695,
                "sellPrice": 1989,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "thargoidpod",
                "stock": 0,
                "demand": 2,
                "buyPrice": 0,
                "meanPrice": 148147,
                "sellPrice": 148753,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "thargoidtissuesampletype6",
                "stock": 0,
                "demand": 2,
                "buyPrice": 0,
                "meanPrice": 70981,
                "sellPrice": 71406,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "thargoidtissuesampletype9a",
                "stock": 0,
                "demand": 2,
                "buyPrice": 0,
                "meanPrice": 496635,
                "sellPrice": 497747,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "thargoidtissuesampletype9b",
                "stock": 0,
                "demand": 2,
                "buyPrice": 0,
                "meanPrice": 271074,
                "sellPrice": 271894,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "thargoidtissuesampletype9c",
                "stock": 0,
                "demand": 2,
                "buyPrice": 0,
                "meanPrice": 138542,
                "sellPrice": 139128,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "thehuttonmug",
                "stock": 0,
                "demand": 0,
                "buyPrice": 102,
                "meanPrice": 7986,
                "sellPrice": 15939,
                "stockBracket": 0,
                "demandBracket": 0
            },
            {
                "name": "tobacco",
                "stock": 0,
                "demand": 14,
                "buyPrice": 0,
                "meanPrice": 5324,
                "sellPrice": 5017,
                "stockBracket": 0,
                "demandBracket": 1
            },
            {
                "name": "unocuppiedescapepod",
                "stock": 0,
                "demand": 2,
                "buyPrice": 0,
                "meanPrice": 3900,
                "sellPrice": 4038,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "usscargoblackbox",
                "stock": 0,
                "demand": 2,
                "buyPrice": 0,
                "meanPrice": 31063,
                "sellPrice": 30909,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "water",
                "stock": 0,
                "demand": 21,
                "buyPrice": 0,
                "meanPrice": 279,
                "sellPrice": 290,
                "stockBracket": 0,
                "demandBracket": 1
            },
            {
                "name": "waterpurifiers",
                "stock": 0,
                "demand": 143,
                "buyPrice": 0,
                "meanPrice": 484,
                "sellPrice": 720,
                "stockBracket": 0,
                "demandBracket": 3
            },
            {
                "name": "wine",
                "stock": 0,
                "demand": 107,
                "buyPrice": 0,
                "meanPrice": 507,
                "sellPrice": 415,
                "stockBracket": 0,
                "demandBracket": 1
            },
            {
                "name": "wreckagecomponents",
                "stock": 0,
                "demand": 10,
                "buyPrice": 0,
                "meanPrice": 9034,
                "sellPrice": 8890,
                "stockBracket": 0,
                "demandBracket": 3
            }
        ],
        "stationName": "Fukuda Metallurgic Complex"
    }
]

class FSDJumpSerializerTestCase(TestCase):

    fixtures = ['user', 'economy', 'system', 'body', 'bgs', 'exploration', 'material', 'mining', 'station']

    @classmethod
    def setUpTestData(cls):
        cls.agent = User.objects.create_user(
            username='FSDJumpSerializerTestCase'
        )

    def test_validate(self):
        for item in FSD_JUMP_TEST_DATA:
            serializer = FSDJumpSerializer(data=item)
            self.assertTrue(serializer.is_valid(), f"Data validation failed: {serializer.errors} for item: {item}")

    def test_create(self):
        for item in FSD_JUMP_TEST_DATA:
            serializer = FSDJumpSerializer(data=item)
            self.assertTrue(serializer.is_valid(), f"Data validation failed: {serializer.errors} for item: {item}")
            fsd_jump = serializer.save(created_by=self.agent, updated_by=self.agent)
            self.assertIsNotNone(fsd_jump.pk, "FSDJump object was not created successfully")
            self.assertEqual(fsd_jump.created_by, self.agent)
            self.assertEqual(fsd_jump.updated_by, self.agent)

class DockedSerializerTestCase(TestCase):
    
    fixtures = ['user', 'economy', 'system', 'body', 'bgs', 'exploration', 'material', 'mining', 'station', 'test_doked_serializer.']

    @classmethod
    def setUpTestData(cls):
        cls.agent = User.objects.create_user(
            username='DockedSerializerTestCase'
        )

    def test_validate(self):
        for item in DOCKED_TEST_DATA:
            serializer = DockedSerializer(data=item)
            self.assertTrue(serializer.is_valid(), f"Data validation failed: {serializer.errors} for item: {item}")

    def test_create(self):
        for item in DOCKED_TEST_DATA:
            serializer = DockedSerializer(data=item)
            self.assertTrue(serializer.is_valid(), f"Data validation failed: {serializer.errors} for item: {item}")
            docked = serializer.save(created_by=self.agent, updated_by=self.agent)
            self.assertIsNotNone(docked.pk, "Docked object was not created successfully")
            self.assertEqual(docked.created_by, self.agent)
            self.assertEqual(docked.updated_by, self.agent)

class LocationSerializerTestCase(TestCase):

    fixtures = ['user', 'economy', 'system', 'body', 'bgs', 'exploration', 'material', 'mining', 'station']
    
    @classmethod
    def setUpTestData(cls):
        cls.agent = User.objects.create_user(
            username='LocationSerializerTestCase'
        )

    def test_validate(self):
        for item in LOCATION_TEST_DATA:
            serializer = LocationSerializer(data=item)
            self.assertTrue(serializer.is_valid(), f"Data validation failed: {serializer.errors} for item: {item}")

    def test_create(self):
        for item in LOCATION_TEST_DATA:
            serializer = LocationSerializer(data=item)
            self.assertTrue(serializer.is_valid(), f"Data validation failed: {serializer.errors} for item: {item}")
            location = serializer.save(created_by=self.agent, updated_by=self.agent)
            self.assertIsNotNone(location.pk, "Location object was not created successfully")
            self.assertEqual(location.created_by, self.agent)
            self.assertEqual(location.updated_by, self.agent)

class CommodityV3SerializerTestCase(TestCase):
    
    fixtures = ['user', 'economy', 'system', 'body', 'bgs', 'exploration', 'material', 'mining', 'station']

    @classmethod
    def setUpTestData(cls):
        cls.agent = User.objects.create_user(
            username='CommodityV3SerializerTestCase'
        )

    def test_validate(self):
        for item in COMMODITY_V3_TEST_DATA:
            serializer = CommodityV3Serializer(data=item)
            self.assertTrue(serializer.is_valid(), f"Data validation failed: {serializer.errors} for item: {item}")

    def test_create(self):
        for item in COMMODITY_V3_TEST_DATA:
            serializer = CommodityV3Serializer(data=item)
            self.assertTrue(serializer.is_valid(), f"Data validation failed: {serializer.errors} for item: {item}")
            commodity = serializer.save(created_by=self.agent, updated_by=self.agent)
            self.assertIsNotNone(commodity.pk, "Commodity object was not created successfully")
            self.assertEqual(commodity.created_by, self.agent)
            self.assertEqual(commodity.updated_by, self.agent)