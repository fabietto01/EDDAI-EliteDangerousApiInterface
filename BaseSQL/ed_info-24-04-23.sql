-- MySQL dump 10.13  Distrib 8.0.27, for Win64 (x86_64)
--
-- Host: 204.216.215.43    Database: ed_info-dev
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping data for table `ed_bgs_faction`
--

LOCK TABLES `ed_bgs_faction` WRITE;
/*!40000 ALTER TABLE `ed_bgs_faction` DISABLE KEYS */;
INSERT INTO `ed_bgs_faction` VALUES (1,NULL,'Independent',''),(2,NULL,'Guardian',''),(3,NULL,'Pilots Federation',''),(4,NULL,'Thargoid',''),(5,NULL,'Alliance',''),(6,NULL,'Empire',''),(7,NULL,'Federation','');
/*!40000 ALTER TABLE `ed_bgs_faction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_bgs_government`
--

LOCK TABLES `ed_bgs_government` WRITE;
/*!40000 ALTER TABLE `ed_bgs_government` DISABLE KEYS */;
INSERT INTO `ed_bgs_government` VALUES (1,NULL,'Anarchy','A',''),(2,NULL,'Dictatorship','C',''),(3,NULL,'Feudal','C',''),(4,NULL,'Patronage','C',''),(5,'PrisonColony','Prison Colony','C',''),(6,NULL,'Theocracy','C',''),(7,NULL,'Corporation','P',''),(8,NULL,'Confederacy','S',''),(9,NULL,'Corporate','S',''),(10,NULL,'Democracy','S',''),(11,NULL,'Cooperative','S',''),(12,NULL,'Communism','S','');
/*!40000 ALTER TABLE `ed_bgs_government` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `ed_bgs_power` WRITE;
/*!40000 ALTER TABLE `ed_bgs_power` DISABLE KEYS */;
INSERT INTO `ed_bgs_power` VALUES (1,'Zemina Torval','',6,1),(2,'Felicia Winters','',7,2),(3,'A. Lavigny-Duval','',6,3),(4,'Aisling Duval','',6,4),(5,'Archon Delaine','',1,5),(6,'Denton Patreus','',6,6),(7,'Edmund Mahon','',5,7),(8,'Li Yong-Rui','',1,8),(9,'Antal','',1,9),(10,'Yuri Grom','',1,10),(11,'Zachary Hudson','',7,11);
/*!40000 ALTER TABLE `ed_bgs_power` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_bgs_powerinsystem`
--

LOCK TABLES `ed_bgs_powerinsystem` WRITE;
/*!40000 ALTER TABLE `ed_bgs_powerinsystem` DISABLE KEYS */;
/*!40000 ALTER TABLE `ed_bgs_powerinsystem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_bgs_powerinsystem_powers`
--

LOCK TABLES `ed_bgs_powerinsystem_powers` WRITE;
/*!40000 ALTER TABLE `ed_bgs_powerinsystem_powers` DISABLE KEYS */;
/*!40000 ALTER TABLE `ed_bgs_powerinsystem_powers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_bgs_powerstate`
--

LOCK TABLES `ed_bgs_powerstate` WRITE;
/*!40000 ALTER TABLE `ed_bgs_powerstate` DISABLE KEYS */;
INSERT INTO `ed_bgs_powerstate` VALUES (1,'HomeSystem','Home System',''),(2,NULL,'Turmoil',''),(3,NULL,'Controlled',''),(4,NULL,'Contested',''),(5,NULL,'Exploited',''),(6,NULL,'Prepared',''),(7,'InPrepareRadius','In Prepare Radius','');
/*!40000 ALTER TABLE `ed_bgs_powerstate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_bgs_state`
--

LOCK TABLES `ed_bgs_state` WRITE;
/*!40000 ALTER TABLE `ed_bgs_state` DISABLE KEYS */;
INSERT INTO `ed_bgs_state` VALUES (1,NULL,'despondent','H',''),(2,NULL,'Unhappy','H',''),(3,NULL,'Discontented','H',''),(4,'Happiness','Happy','H',''),(5,NULL,'Elated','H',''),(6,NULL,'Famine','E',''),(7,NULL,'Bust','E',''),(8,NULL,'None','E',''),(9,NULL,'Boom','E',''),(10,NULL,'Investment','E',''),(11,NULL,'Lockdown','S',''),(12,'CivilUnrest','Civil Unrest','S',''),(13,NULL,'None','S',''),(14,'PirateAttack','Pirate Attack','O',''),(15,'PublicHoliday','Public Holiday','O',''),(16,NULL,'Expansion','O',''),(17,NULL,'Drought','O',''),(18,'Election','Elections','O',''),(19,'InfrastructureFailure','Infrastructure Failure','O',''),(20,NULL,'War','O',''),(21,NULL,'Outbreak','O',''),(22,'CivilWar','Civil War','O',''),(23,NULL,'Blight','O',''),(24,'CivilLiberty','Civil Liberty','S',''),(25,NULL,'Retreat','O',''),(26,'Terrorism','Terrorist Attack','O',''),(27,'NaturalDisaster','Natural Disaster','O','');
/*!40000 ALTER TABLE `ed_bgs_state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_body_atmospheretype`
--

LOCK TABLES `ed_body_atmospheretype` WRITE;
/*!40000 ALTER TABLE `ed_body_atmospheretype` DISABLE KEYS */;
INSERT INTO `ed_body_atmospheretype` VALUES (1,'None','No atmosphere',''),(2,NULL,'Suitable for water-based life',''),(3,'AmmoniaAndOxygen','Ammonia and oxygen',''),(4,NULL,'Ammonia',''),(5,NULL,'Water',''),(6,'CarbonDioxide','Carbon dioxide',''),(7,'SulphurDioxide','Sulphur dioxide',''),(8,NULL,'Nitrogen',''),(9,'WaterRich','Water-rich',''),(10,'MethaneRich','Methane-rich',''),(11,'AmmoniaRich','Ammonia-rich',''),(12,'CarbonDioxideRich','Carbon dioxide-rich',''),(13,NULL,'Methane',''),(14,NULL,'Helium',''),(15,'SilicateVapour','Silicate vapour',''),(16,'MetallicVapour','Metallic vapour',''),(17,'NeonRich','Neon-rich',''),(18,'ArgonRich','Argon-rich',''),(19,NULL,'Neon',''),(20,NULL,'Argon',''),(21,NULL,'Oxygen',''),(22,'AmmoniaOxygen','Ammonia Oxygen',''),(23,'EarthLike','Earth Like','');
/*!40000 ALTER TABLE `ed_body_atmospheretype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_body_planettype`
--

LOCK TABLES `ed_body_planettype` WRITE;
/*!40000 ALTER TABLE `ed_body_planettype` DISABLE KEYS */;
INSERT INTO `ed_body_planettype` VALUES (1,'Metal rich body',''),(2,'High metal content body',''),(3,'Rocky body',''),(4,'Icy body',''),(5,'Rocky ice body',''),(6,'Earthlike body',''),(7,'Water world',''),(8,'Ammonia world',''),(9,'Water giant',''),(10,'Water giant with life',''),(11,'Gas giant with water based life',''),(12,'Gas giant with ammonia based life',''),(13,'Sudarsky class I gas giant',''),(14,'Sudarsky class II gas giant',''),(15,'Sudarsky class III gas giant',''),(16,'Sudarsky class IV gas giant',''),(17,'Sudarsky class V gas giant',''),(18,'Helium rich gas giant',''),(19,'Helium gas giant','');
/*!40000 ALTER TABLE `ed_body_planettype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_body_starluminosity`
--

LOCK TABLES `ed_body_starluminosity` WRITE;
/*!40000 ALTER TABLE `ed_body_starluminosity` DISABLE KEYS */;
INSERT INTO `ed_body_starluminosity` VALUES (1,'0',''),(2,'I',''),(3,'Ia0',''),(4,'Ia',''),(5,'Ib',''),(6,'Iab',''),(7,'II',''),(8,'IIa',''),(9,'IIab',''),(10,'IIb',''),(11,'III',''),(12,'IIIa',''),(13,'IIIab',''),(14,'IIIb',''),(15,'IV',''),(16,'IVa',''),(17,'IVab',''),(18,'IVb',''),(19,'V',''),(20,'Va',''),(21,'Vab',''),(22,'Vb',''),(23,'Vz',''),(24,'VI',''),(25,'VII','');
/*!40000 ALTER TABLE `ed_body_starluminosity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_body_startype`
--

LOCK TABLES `ed_body_startype` WRITE;
/*!40000 ALTER TABLE `ed_body_startype` DISABLE KEYS */;
INSERT INTO `ed_body_startype` VALUES (1,'O','',NULL),(2,'B','',NULL),(3,'A','',NULL),(4,'F','',NULL),(5,'G','',NULL),(6,'K','',NULL),(7,'M','',NULL),(8,'L','',NULL),(9,'T','',NULL),(10,'Y','',NULL),(11,'UN','',NULL),(12,'UNA','',NULL),(13,'TTS','',NULL),(14,'WO','',NULL),(15,'wc','',NULL),(16,'WN','',NULL),(17,'WNC','',NULL),(18,'DC','',NULL),(19,'DA','',NULL),(20,'M Red Giant','','M_RedGiant'),(21,'N','',NULL),(22,'S','',NULL),(23,'CN','',NULL),(24,'DQ','',NULL),(25,'D','',NULL),(26,'DAB','',NULL),(27,'DBV','',NULL),(28,'H','',NULL),(29,'AeBe','',NULL),(32,'DCV','',NULL),(33,'K OrangeGiant','','K_OrangeGiant'),(38,'MS','',NULL),(39,'DB','',NULL),(40,'A Blue White Super Giant','','A_BlueWhiteSuperGiant');
/*!40000 ALTER TABLE `ed_body_startype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_body_volcanism`
--

LOCK TABLES `ed_body_volcanism` WRITE;
/*!40000 ALTER TABLE `ed_body_volcanism` DISABLE KEYS */;
INSERT INTO `ed_body_volcanism` VALUES (1,'Minor Water Magma volcanism','','minor water magma volcanism'),(2,'Major Water Magma volcanism','','major water magma volcanism'),(3,'Minor Sulphur Dioxide Magma volcanism','','minor sulphur dioxide magma volcanism'),(4,'Minor Ammonia Magma volcanism','','minor ammonia magma volcanism'),(5,'Minor Methane Magma volcanism','','minor methane magma volcanism'),(6,'Minor Nitrogen Magma volcanism','','minor nitrogen magma volcanism'),(7,'Minor Silicate Magma volcanism','','minor silicate magma volcanism'),(8,'Minor Metallic Magma volcanism','','minor metallic magma volcanism'),(9,'Minor Water Geysers volcanism','','minor water geysers volcanism'),(10,'Minor Carbon Dioxide Geysers volcanism','','minor carbon dioxide geysers volcanism'),(11,'Minor Ammonia Geysers volcanism','','minor ammonia geysers volcanism'),(12,'Minor Methane Geysers volcanism','','minor methane geysers volcanism'),(13,'Minor Nitrogen Geysers volcanism','','minor nitrogen geysers volcanism'),(14,'Minor Helium Geysers volcanism','','minor helium geysers volcanism'),(15,'Minor Silicate Vapour Geysers volcanism','','minor silicate vapour geysers volcanism'),(16,'Major Silicate Vapour Geysers volcanism','','major silicate vapour geysers volcanism'),(17,'Major Sulphur Dioxide Magma volcanism','','major sulphur dioxide magma volcanism'),(18,'Major Ammonia Magma volcanism','','major ammonia magma volcanism'),(19,'Major Methane Magma volcanism','','major methane magma volcanism'),(20,'Major Nitrogen Magma volcanism','','major nitrogen magma volcanism'),(21,'Major Silicate Magma volcanism','','major silicate magma volcanism'),(22,'Major Metallic Magma volcanism','','major metallic magma volcanism'),(23,'Major Water Geysers volcanism','','major water geysers volcanism'),(24,'Major Carbon Dioxide Geysers volcanism','','major carbon dioxide geysers volcanism'),(25,'Major Ammonia Geysers volcanism','','major ammonia geysers volcanism'),(26,'Major Methane Geysers volcanism','','major methane geysers volcanism'),(27,'Major Nitrogen Geysers volcanism','','major nitrogen geysers volcanism'),(28,'Major Helium Geysers volcanism','','major helium geysers volcanism'),(29,'Water Magma volcanism','','water magma volcanism'),(30,'Sulphur Dioxide Magma volcanism','','sulphur dioxide magma volcanism'),(31,'Ammonia Magma volcanism','','ammonia magma volcanism'),(32,'Methane Magma volcanism','','methane magma volcanism'),(33,'Nitrogen Magma volcanism','','nitrogen magma volcanism'),(34,'Silicate Magma volcanism','','silicate magma volcanism'),(35,'Metallic Magma volcanism','','metallic magma volcanism'),(36,'Water Geysers volcanism','','water geysers volcanism'),(37,'Carbon Dioxide Geysers volcanism','','carbon dioxide geysers volcanism'),(38,'Ammonia Geysers volcanism','','ammonia geysers volcanism'),(39,'Methane Geysers volcanism','','methane geysers volcanism'),(40,'Nitrogen Geysers volcanism','','nitrogen geysers volcanism'),(41,'Helium Geysers volcanism','','helium geysers volcanism'),(42,'Silicate Vapour Geysers volcanism','','silicate vapour geysers volcanism'),(43,'Minor Rocky Magma volcanism','','minor rocky magma volcanism'),(44,'Rocky Magma volcanism','','rocky magma volcanism'),(45,'Major Rocky Magma volcanism','','major rocky magma volcanism'),(46,'No volcanism','','');
/*!40000 ALTER TABLE `ed_body_volcanism` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_economy_commodity`
--

LOCK TABLES `ed_economy_commodity` WRITE;
/*!40000 ALTER TABLE `ed_economy_commodity` DISABLE KEYS */;
INSERT INTO `ed_economy_commodity` VALUES (1,NULL,'advancedcatalysers','',3039),(2,NULL,'advancedmedicines',NULL,1485),(3,NULL,'advert1',NULL,0),(4,NULL,'aerialedenapple',NULL,0),(5,NULL,'agriculturalmedicines',NULL,1231),(6,NULL,'agronomictreatment',NULL,3105),(7,NULL,'alacarakmoskinart',NULL,0),(8,NULL,'albinoquechuamammoth',NULL,0),(9,NULL,'alexandrite',NULL,217356),(10,NULL,'algae',NULL,356),(11,NULL,'alieneggs',NULL,0),(12,NULL,'altairianskin',NULL,0),(13,NULL,'aluminium',NULL,551),(14,NULL,'alyabodilysoap',NULL,0),(15,NULL,'ancientcasket',NULL,0),(16,NULL,'ancientkey',NULL,0),(17,NULL,'ancientorb',NULL,0),(18,NULL,'ancientrelic',NULL,0),(19,NULL,'ancientrelictg',NULL,0),(20,NULL,'ancienttablet',NULL,0),(21,NULL,'ancienttotem',NULL,0),(22,NULL,'ancienturn',NULL,0),(23,NULL,'anduligafireworks',NULL,0),(24,NULL,'animalmeat',NULL,1539),(25,NULL,'animalmonitors',NULL,537),(26,NULL,'antiquejewellery',NULL,0),(27,NULL,'anynacoffee',NULL,0),(28,NULL,'apavietii',NULL,0),(29,NULL,'aquaponicsystems',NULL,524),(30,NULL,'aroucaconventualsweets',NULL,0),(31,NULL,'articulationmotors',NULL,7589),(32,NULL,'assaultplans',NULL,0),(33,NULL,'atmosphericextractors',NULL,571),(34,NULL,'autofabricators',NULL,3826),(35,NULL,'azcancriformula42',NULL,0),(36,NULL,'bakedgreebles',NULL,0),(37,NULL,'baltahsinevacuumkrill',NULL,0),(38,NULL,'bankiamphibiousleather',NULL,0),(39,NULL,'basicmedicines',NULL,493),(40,NULL,'bastsnakegin',NULL,0),(41,NULL,'bauxite',NULL,1140),(42,NULL,'beer',NULL,430),(43,NULL,'belalansrayleather',NULL,0),(44,NULL,'benitoite',NULL,149459),(45,NULL,'bertrandite',NULL,18817),(46,NULL,'beryllium',NULL,8242),(47,NULL,'bioreducinglichen',NULL,1204),(48,NULL,'biowaste',NULL,358),(49,NULL,'bismuth',NULL,2440),(50,NULL,'bluemilk',NULL,0),(51,NULL,'bootlegliquor',NULL,779),(52,NULL,'bromellite',NULL,30427),(53,NULL,'buckyballbeermats',NULL,0),(54,NULL,'buildingfabricators',NULL,2311),(55,NULL,'burnhambiledistillate',NULL,0),(56,NULL,'cd75catcoffee',NULL,0),(57,NULL,'centaurimegagin',NULL,10217),(58,NULL,'ceramiccomposites',NULL,415),(59,NULL,'ceremonialheiketea',NULL,0),(60,NULL,'cetiaepyornisegg',NULL,0),(61,NULL,'cetirabbits',NULL,0),(62,NULL,'chameleoncloth',NULL,0),(63,NULL,'chateaudeaegaeon',NULL,0),(64,NULL,'chemicalwaste',NULL,672),(65,NULL,'cherbonesbloodcrystals',NULL,0),(66,NULL,'chieridanimarinepaste',NULL,0),(67,NULL,'classifiedexperimentalequipment',NULL,0),(68,NULL,'clothing',NULL,546),(69,NULL,'cmmcomposite',NULL,5987),(70,NULL,'cobalt',NULL,3761),(71,NULL,'coffee',NULL,1498),(72,NULL,'coltan',NULL,6163),(73,NULL,'comercialsamples',NULL,0),(74,NULL,'computercomponents',NULL,775),(75,NULL,'conductivefabrics',NULL,709),(76,NULL,'consumertechnology',NULL,6691),(77,NULL,'coolinghoses',NULL,1886),(78,NULL,'copper',NULL,689),(79,NULL,'coquimspongiformvictuals',NULL,0),(80,NULL,'cropharvesters',NULL,2230),(81,NULL,'cryolite',NULL,12172),(82,NULL,'crystallinespheres',NULL,0),(83,NULL,'damnacarapaces',NULL,0),(84,NULL,'datacore',NULL,0),(85,NULL,'deltaphoenicispalms',NULL,0),(86,NULL,'deuringastruffles',NULL,0),(87,NULL,'diagnosticsensor',NULL,6727),(88,NULL,'diplomaticbag',NULL,0),(89,NULL,'disomacorn',NULL,0),(90,NULL,'domesticappliances',NULL,740),(91,NULL,'duradrives',NULL,0),(92,NULL,'earthrelics',NULL,0),(93,NULL,'eleuthermals',NULL,0),(94,NULL,'emergencypowercells',NULL,2368),(95,NULL,'encripteddatastorage',NULL,0),(96,NULL,'encryptedcorrespondence',NULL,0),(97,NULL,'eraninpearlwhisky',NULL,0),(98,NULL,'eshuumbrellas',NULL,0),(99,NULL,'esusekucaviar',NULL,0),(100,NULL,'ethgrezeteabuds',NULL,0),(101,NULL,'evacuationshelter',NULL,523),(102,NULL,'exhaustmanifold',NULL,1873),(103,NULL,'explosives',NULL,513),(104,NULL,'fish',NULL,649),(105,NULL,'foodcartridges',NULL,266),(106,NULL,'fossilremnants',NULL,0),(107,NULL,'fruitandvegetables',NULL,509),(108,NULL,'fujintea',NULL,0),(109,NULL,'galactictravelguide',NULL,0),(110,NULL,'gallite',NULL,11915),(111,NULL,'gallium',NULL,5202),(112,NULL,'geawendancedust',NULL,0),(113,NULL,'genebank',NULL,0),(114,NULL,'geologicalequipment',NULL,1886),(115,NULL,'geologicalsamples',NULL,0),(116,NULL,'gerasiangueuzebeer',NULL,0),(117,NULL,'giantirukamasnails',NULL,0),(118,NULL,'giantverrix',NULL,0),(119,NULL,'gilyasignatureweapons',NULL,0),(120,NULL,'gold',NULL,47609),(121,NULL,'gomanyauponcoffee',NULL,0),(122,NULL,'goslarite',NULL,5978),(123,NULL,'grain',NULL,411),(124,NULL,'grandidierite',NULL,197373),(125,NULL,'haidneblackbrew',NULL,0),(126,NULL,'harmasilversearum',NULL,0),(127,NULL,'havasupaidreamcatcher',NULL,0),(128,NULL,'hazardousenvironmentsuits',NULL,570),(129,NULL,'heatsinkinterlink',NULL,2100),(130,NULL,'heliostaticfurnaces',NULL,434),(131,NULL,'helvetitjpearls',NULL,0),(132,NULL,'hip10175bushmeat',NULL,0),(133,NULL,'hip41181squid',NULL,0),(134,NULL,'hiporganophosphates',NULL,0),(135,NULL,'hnshockmount',NULL,1923),(136,NULL,'holvaduellingblades',NULL,0),(137,NULL,'honestypills',NULL,0),(138,NULL,'hr7221wheat',NULL,0),(139,NULL,'hydrogenfuel',NULL,113),(140,NULL,'hydrogenperoxide',NULL,3161),(141,NULL,'indibourbon',NULL,0),(142,NULL,'indite',NULL,11389),(143,NULL,'indium',NULL,5844),(144,NULL,'insulatingmembrane',NULL,10724),(145,NULL,'iondistributor',NULL,2367),(146,NULL,'jadeite',NULL,42385),(147,NULL,'jaquesquinentianstill',NULL,0),(148,NULL,'jaradharrepuzzlebox',NULL,0),(149,NULL,'jarouarice',NULL,0),(150,NULL,'jotunmookah',NULL,0),(151,NULL,'kachiriginleaches',NULL,0),(152,NULL,'kamorinhistoricweapons',NULL,0),(153,NULL,'karetiicouture',NULL,0),(154,NULL,'karsukilocusts',NULL,0),(155,NULL,'kinagoinstruments',NULL,0),(156,NULL,'konggaale',NULL,8310),(157,NULL,'korrokungpellets',NULL,0),(158,NULL,'landmines',NULL,4796),(159,NULL,'lanthanum',NULL,8706),(160,NULL,'largeexplorationdatacash',NULL,0),(161,NULL,'lavianbrandy',NULL,0),(162,NULL,'leather',NULL,435),(163,NULL,'leestianeviljuice',NULL,0),(164,NULL,'lepidolite',NULL,772),(165,NULL,'lftvoidextractcoffee',NULL,0),(166,NULL,'liquidoxygen',NULL,1473),(167,NULL,'liquor',NULL,879),(168,NULL,'lithium',NULL,1771),(169,NULL,'lithiumhydroxide',NULL,5673),(170,NULL,'livehecateseaworms',NULL,0),(171,NULL,'lowtemperaturediamond',NULL,106382),(172,NULL,'ltthypersweet',NULL,0),(173,NULL,'lyraeweed',NULL,0),(174,NULL,'m3_tissuesample_membrane',NULL,0),(175,NULL,'m3_tissuesample_mycelium',NULL,0),(176,NULL,'m3_tissuesample_spores',NULL,0),(177,NULL,'m_tissuesample_fluid',NULL,0),(178,NULL,'m_tissuesample_nerves',NULL,0),(179,NULL,'m_tissuesample_soft',NULL,0),(180,NULL,'magneticemittercoil',NULL,1357),(181,NULL,'marinesupplies',NULL,4136),(182,NULL,'mechucoshightea',NULL,0),(183,NULL,'medbstarlube',NULL,0),(184,NULL,'medicaldiagnosticequipment',NULL,3075),(185,NULL,'metaalloys',NULL,195459),(186,NULL,'methaneclathrate',NULL,1650),(187,NULL,'methanolmonohydratecrystals',NULL,2479),(188,NULL,'microcontrollers',NULL,5590),(189,NULL,'militarygradefabrics',NULL,985),(190,NULL,'mineralextractors',NULL,801),(191,NULL,'mineraloil',NULL,423),(192,NULL,'modularterminals',NULL,2476),(193,NULL,'moissanite',NULL,24834),(194,NULL,'mokojingbeastfeast',NULL,0),(195,NULL,'momusbogspaniel',NULL,0),(196,NULL,'monazite',NULL,201026),(197,NULL,'mukusubiichitinos',NULL,0),(198,NULL,'mulachigiantfungus',NULL,0),(199,NULL,'musgravite',NULL,198692),(200,NULL,'mutomimager',NULL,6313),(201,NULL,'mysteriousidol',NULL,0),(202,NULL,'nanobreakers',NULL,2367),(203,NULL,'nanomedicines',NULL,0),(204,NULL,'naturalfabrics',NULL,687),(205,NULL,'neofabricinsulation',NULL,5979),(206,NULL,'neritusberries',NULL,0),(207,NULL,'nerveagents',NULL,13514),(208,NULL,'ngadandarifireopals',NULL,0),(209,NULL,'ngunamodernantiques',NULL,0),(210,NULL,'njangarisaddles',NULL,0),(211,NULL,'noneuclidianexotanks',NULL,0),(212,NULL,'nonlethalweapons',NULL,1943),(213,NULL,'ochoengchillies',NULL,0),(214,NULL,'onionheadc',NULL,4828),(215,NULL,'opal',NULL,135339),(216,NULL,'ophiuchiexinoartefacts',NULL,0),(217,NULL,'orrerianviciousbrew',NULL,0),(218,NULL,'osmium',NULL,45210),(219,NULL,'p_particulatesample',NULL,0),(220,NULL,'painite',NULL,53032),(221,NULL,'palladium',NULL,50639),(222,NULL,'pantaaprayersticks',NULL,0),(223,NULL,'pavoniseargrubs',NULL,0),(224,NULL,'performanceenhancers',NULL,6790),(225,NULL,'personalgifts',NULL,0),(226,NULL,'personalweapons',NULL,4735),(227,NULL,'pesticides',NULL,437),(228,NULL,'platinum',NULL,58272),(229,NULL,'platinumaloy',NULL,0),(230,NULL,'polymers',NULL,376),(231,NULL,'powerconverter',NULL,1435),(232,NULL,'powergenerators',NULL,2466),(233,NULL,'powergridassembly',NULL,2659),(234,NULL,'powertransferconduits',NULL,2212),(235,NULL,'praseodymium',NULL,8620),(236,NULL,'preciousgems',NULL,0),(237,NULL,'progenitorcells',NULL,6751),(238,NULL,'pyrophyllite',NULL,11536),(239,NULL,'radiationbaffle',NULL,1787),(240,NULL,'rajukrustoves',NULL,0),(241,NULL,'rapabaosnakeskins',NULL,0),(242,NULL,'reactivearmour',NULL,2224),(243,NULL,'reinforcedmountingplate',NULL,2454),(244,NULL,'resonatingseparators',NULL,5937),(245,NULL,'rhodplumsite',NULL,176882),(246,NULL,'robotics',NULL,2019),(247,NULL,'rockforthfertiliser',NULL,0),(248,NULL,'rutile',NULL,2083),(249,NULL,'s6_tissuesample_cells',NULL,0),(250,NULL,'s6_tissuesample_coenosarc',NULL,0),(251,NULL,'s6_tissuesample_mesoglea',NULL,0),(252,NULL,'s9_tissuesample_shell',NULL,0),(253,NULL,'s_tissuesample_cells',NULL,0),(254,NULL,'s_tissuesample_core',NULL,0),(255,NULL,'s_tissuesample_surface',NULL,0),(256,NULL,'samarium',NULL,25853),(257,NULL,'sanumameat',NULL,0),(258,NULL,'sap8corecontainer',NULL,0),(259,NULL,'saxonwine',NULL,0),(260,NULL,'scientificresearch',NULL,0),(261,NULL,'scientificsamples',NULL,0),(262,NULL,'scrap',NULL,300),(263,NULL,'semiconductors',NULL,1136),(264,NULL,'serendibite',NULL,172781),(265,NULL,'shanscharisorchid',NULL,0),(266,NULL,'silver',NULL,37223),(267,NULL,'skimercomponents',NULL,1119),(268,NULL,'smallexplorationdatacash',NULL,0),(269,NULL,'soontillrelics',NULL,0),(270,NULL,'sothiscrystallinegold',NULL,0),(271,NULL,'spacepioneerrelics',NULL,0),(272,NULL,'structuralregulators',NULL,1933),(273,NULL,'superconductors',NULL,6678),(274,NULL,'surfacestabilisers',NULL,727),(275,NULL,'survivalequipment',NULL,684),(276,NULL,'syntheticfabrics',NULL,416),(277,NULL,'syntheticmeat',NULL,440),(278,NULL,'syntheticreagents',NULL,6651),(279,NULL,'taaffeite',NULL,52091),(280,NULL,'tacticaldata',NULL,0),(281,NULL,'tanmarktranquiltea',NULL,0),(282,NULL,'tantalum',NULL,4043),(283,NULL,'taurichimes',NULL,0),(284,NULL,'tea',NULL,1695),(285,NULL,'telemetrysuite',NULL,3215),(286,NULL,'terrainenrichmentsystems',NULL,4928),(287,NULL,'thallium',NULL,3744),(288,NULL,'thargoidgeneratortissuesample',NULL,0),(289,NULL,'thargoidheart',NULL,0),(290,NULL,'thargoidscouttissuesample',NULL,0),(291,NULL,'thargoidtissuesampletype1',NULL,0),(292,NULL,'thargoidtissuesampletype2',NULL,0),(293,NULL,'thargoidtissuesampletype3',NULL,0),(294,NULL,'thargoidtissuesampletype4',NULL,0),(295,NULL,'thargoidtissuesampletype5',NULL,0),(296,NULL,'thehuttonmug',NULL,7986),(297,NULL,'thermalcoolingunits',NULL,3761),(298,NULL,'thorium',NULL,11316),(299,NULL,'thrutiscream',NULL,0),(300,NULL,'tiegfriessynthsilk',NULL,0),(301,NULL,'timecapsule',NULL,0),(302,NULL,'tiolcewaste2pasteunits',NULL,0),(303,NULL,'titanium',NULL,1208),(304,NULL,'toxandjivirocide',NULL,0),(305,NULL,'transgeniconionhead',NULL,0),(306,NULL,'tritium',NULL,51707),(307,NULL,'unknownartifact',NULL,0),(308,NULL,'unknownartifact2',NULL,0),(309,NULL,'unknownartifact3',NULL,0),(310,NULL,'unknownbiologicalmatter',NULL,0),(311,NULL,'unknownresin',NULL,0),(312,NULL,'unknowntechnologysamples',NULL,0),(313,NULL,'unocuppiedescapepod',NULL,3900),(314,NULL,'unstabledatacore',NULL,0),(315,NULL,'uraninite',NULL,2958),(316,NULL,'uranium',NULL,2826),(317,NULL,'usscargorareartwork',NULL,16808),(318,NULL,'uszaiantreegrub',NULL,0),(319,NULL,'utgaroarmillenialeggs',NULL,0),(320,NULL,'uzumokulowgwings',NULL,0),(321,NULL,'vanayequirhinofur',NULL,0),(322,NULL,'vegaslimweed',NULL,0),(323,NULL,'vherculisbodyrub',NULL,0),(324,NULL,'vidavantianlace',NULL,0),(325,NULL,'volkhabbeedrones',NULL,0),(326,NULL,'water',NULL,279),(327,NULL,'waterpurifiers',NULL,484),(328,NULL,'watersofshintara',NULL,13711),(329,NULL,'wheemetewheatcakes',NULL,0),(330,NULL,'wine',NULL,507),(331,NULL,'witchhaulkobebeef',NULL,0),(332,NULL,'wulpahyperboresystems',NULL,0),(333,NULL,'wuthielokufroth',NULL,0),(334,NULL,'xihecompanions',NULL,0),(335,NULL,'zeesszeantglue',NULL,0),(336,NULL,'damagedescapepod',NULL,16966),(337,NULL,'hostage',NULL,34605),(338,NULL,'occupiedcryopod',NULL,30364),(339,NULL,'personaleffects',NULL,9544),(340,NULL,'tobacco',NULL,5324),(341,NULL,'usscargoblackbox',NULL,31063),(342,NULL,'wreckagecomponents',NULL,9034),(343,NULL,'basicnarcotics',NULL,10124),(344,NULL,'combatstabilisers',NULL,3652),(345,NULL,'imperialslaves',NULL,17493),(346,NULL,'battleweapons',NULL,7441),(347,NULL,'masterchefs',NULL,0),(348,NULL,'kamitracigars',NULL,0),(349,NULL,'rusanioldsmokey',NULL,0),(350,NULL,'yasokondileaf',NULL,0),(351,NULL,'onionhead',NULL,0),(352,NULL,'onionheada',NULL,0),(353,NULL,'onionheadb',NULL,0),(354,NULL,'hip118311swarm',NULL,0),(355,NULL,'tarachtorspice',NULL,0),(356,NULL,'aganipperush',NULL,0),(357,NULL,'borasetanipathogenetics',NULL,0),(358,NULL,'animaleffigies',NULL,0),(359,NULL,'motronaexperiencejelly',NULL,0),(360,NULL,'slaves',NULL,13155),(361,NULL,'terramaterbloodbores',NULL,0),(362,NULL,'wolf1301fesh',NULL,0),(363,NULL,'usscargomilitaryplans',NULL,0),(364,NULL,'prohibitedresearchmaterials',NULL,0),(365,NULL,'trinketsoffortune',NULL,0),(366,NULL,'usscargorebeltransmissions',NULL,0),(367,NULL,'thargoidtissuesampletype6','',70981),(368,NULL,'thargoidtissuesampletype9a','',496635),(369,NULL,'thargoidtissuesampletype9b','',271074),(370,NULL,'thargoidtissuesampletype9c','',138542),(371,NULL,'thargoidtissuesampletype10a','',0),(372,NULL,'thargoidtissuesampletype10c','',0),(373,NULL,'thargoidtissuesampletype10b','',0);
/*!40000 ALTER TABLE `ed_economy_commodity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_economy_economy`
--

LOCK TABLES `ed_economy_economy` WRITE;
/*!40000 ALTER TABLE `ed_economy_economy` DISABLE KEYS */;
INSERT INTO `ed_economy_economy` VALUES (1,NULL,'Extraction',''),(2,NULL,'Refinery',''),(3,NULL,'Industrial',''),(4,'HighTech','High Tech',''),(5,'Agri','Agriculture',''),(6,NULL,'Terraforming',''),(7,NULL,'Tourism',''),(8,NULL,'Service',''),(9,NULL,'Military',''),(10,NULL,'Colony',''),(11,NULL,'Rescue',''),(12,NULL,'Damaged',''),(13,NULL,'Repair',''),(14,'PrivateEnterprise','Private Enterprise',''),(15,'Carrier','Carrier','');
/*!40000 ALTER TABLE `ed_economy_economy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_exploration_samplesignals`
--

LOCK TABLES `ed_exploration_samplesignals` WRITE;
/*!40000 ALTER TABLE `ed_exploration_samplesignals` DISABLE KEYS */;
INSERT INTO `ed_exploration_samplesignals` VALUES (1,'$Codex_Ent_Brancae_Name;','Brancae'),(2,'$Codex_Ent_Bacterial_Genus_Name;','Bacterial'),(3,'$Codex_Ent_Tubus_Genus_Name;','Tubus'),(4,'$Codex_Ent_Shrubs_Genus_Name;','Shrubs'),(5,'$Codex_Ent_Tussocks_Genus_Name;','Tussocks'),(6,'$Codex_Ent_Cactoid_Genus_Name;','Cactoid'),(7,'$Codex_Ent_Conchas_Genus_Name;','Conchas'),(8,'$Codex_Ent_Fungoids_Genus_Name;','Fungoids'),(9,'$Codex_Ent_Osseus_Genus_Name;','Osseus'),(10,'$Codex_Ent_Recepta_Genus_Name;','Recepta'),(11,'$Codex_Ent_Fonticulus_Genus_Name;','Fonticulus'),(12,'$Codex_Ent_Ground_Struct_Ice_Name;','Ground'),(13,'$Codex_Ent_Cone_Name;','Cone'),(14,'$Codex_Ent_Stratum_Genus_Name;','Stratum');
/*!40000 ALTER TABLE `ed_exploration_samplesignals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_exploration_signalsignals`
--

LOCK TABLES `ed_exploration_signalsignals` WRITE;
/*!40000 ALTER TABLE `ed_exploration_signalsignals` DISABLE KEYS */;
INSERT INTO `ed_exploration_signalsignals` VALUES (1,'$SAA_SignalType_Biological;','Biological'),(2,'$SAA_SignalType_Guardian;','Guardian'),(3,'$SAA_SignalType_Geological;','Geological'),(4,'$SAA_SignalType_Human;','Human');
/*!40000 ALTER TABLE `ed_exploration_signalsignals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_material_material`
--

LOCK TABLES `ed_material_material` WRITE;
/*!40000 ALTER TABLE `ed_material_material` DISABLE KEYS */;
INSERT INTO `ed_material_material` VALUES (1,NULL,'Antimony','ra',4,''),(2,NULL,'Arsenic','ra',2,''),(3,NULL,'Boron','ra',1,''),(4,NULL,'Cadmium','ra',3,''),(5,NULL,'Carbon','ra',1,''),(6,NULL,'Chromium','ra',2,''),(7,NULL,'Germanium','ra',2,''),(8,NULL,'Iron','ra',1,''),(9,NULL,'Lead','ra',5,''),(10,NULL,'Manganese','ra',2,''),(11,NULL,'Mercury','ra',3,''),(12,NULL,'Molybdenum','ra',3,''),(13,NULL,'Nickel','ra',5,''),(14,NULL,'Niobium','ra',3,''),(15,NULL,'Phosphorus','ra',5,''),(16,NULL,'Polonium','ra',4,''),(17,NULL,'Rhenium','ra',5,''),(18,NULL,'Ruthenium','ra',4,''),(19,NULL,'Selenium','ra',4,''),(20,NULL,'Sulphur','ra',5,''),(21,NULL,'Technetium','ra',4,''),(22,NULL,'Tellurium','ra',4,''),(23,NULL,'Tin','ra',3,''),(24,NULL,'Tungsten','ra',3,''),(25,NULL,'Vanadium','ra',2,''),(26,NULL,'Yttrium','ra',4,''),(27,NULL,'Zinc','ra',2,''),(28,NULL,'Zirconium','ra',2,'');
/*!40000 ALTER TABLE `ed_material_material` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_mining_hotspotsignals`
--

LOCK TABLES `ed_mining_hotspotsignals` WRITE;
/*!40000 ALTER TABLE `ed_mining_hotspotsignals` DISABLE KEYS */;
INSERT INTO `ed_mining_hotspotsignals` VALUES (1,NULL,'Alexandrite'),(2,NULL,'Benitoite'),(3,NULL,'Bromellite'),(4,NULL,'Grandidierite'),(5,'LowTemperatureDiamond','Low Temperature Diamond'),(6,NULL,'Monazite'),(7,NULL,'Musgravite'),(8,NULL,'Opal'),(9,NULL,'Painite'),(10,NULL,'Platinum'),(11,NULL,'Rhodplumsite'),(12,NULL,'Rutile'),(13,NULL,'Serendibite'),(14,'tritium','Tritium');
/*!40000 ALTER TABLE `ed_mining_hotspotsignals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_station_service`
--

LOCK TABLES `ed_station_service` WRITE;
/*!40000 ALTER TABLE `ed_station_service` DISABLE KEYS */;
INSERT INTO `ed_station_service` VALUES (1,NULL,'dock',''),(2,NULL,'autodock',''),(3,NULL,'commodities',NULL),(4,NULL,'contacts',NULL),(5,NULL,'exploration',NULL),(6,NULL,'missions',NULL),(7,NULL,'outfitting',NULL),(8,NULL,'crewlounge',NULL),(9,NULL,'rearm',NULL),(10,NULL,'refuel',NULL),(11,NULL,'repair',NULL),(12,NULL,'shipyard',NULL),(13,NULL,'tuning',NULL),(14,NULL,'engineer',NULL),(15,NULL,'missionsgenerated',NULL),(16,NULL,'flightcontroller',NULL),(17,NULL,'stationoperations',NULL),(18,NULL,'powerplay',NULL),(19,NULL,'searchrescue',NULL),(20,NULL,'stationMenu',NULL),(21,NULL,'shop',NULL),(22,NULL,'livery',NULL),(23,NULL,'socialspace',NULL),(24,NULL,'bartender',NULL),(25,NULL,'vistagenomics',NULL),(26,NULL,'pioneersupplies',NULL),(27,NULL,'apexinterstellar',NULL),(28,NULL,'frontlinesolutions',NULL),(29,NULL,'facilitator',NULL),(30,NULL,'ondockmission',NULL),(31,NULL,'blackmarket',NULL),(32,NULL,'carriermanagement',NULL),(33,NULL,'carrierfuel',NULL),(34,NULL,'voucherredemption',NULL),(35,NULL,'techBroker',NULL),(36,NULL,'materialtrader',NULL),(37,NULL,'carriervendor',NULL),(38,NULL,'modulepacks',NULL);
/*!40000 ALTER TABLE `ed_station_service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_station_stationtype`
--

LOCK TABLES `ed_station_stationtype` WRITE;
/*!40000 ALTER TABLE `ed_station_stationtype` DISABLE KEYS */;
INSERT INTO `ed_station_stationtype` VALUES (1,'FleetCarrier','Fleet Carrier',''),(2,'OnFootSettlement','On Foot Settlement',''),(3,NULL,'Coriolis',''),(4,NULL,'Outpost',''),(5,NULL,'Orbis',''),(6,'CraterOutpost','Crater Outpost',''),(7,'Ocellus','Ocellus',''),(8,'AsteroidBase','Asteroid Base',''),(9,'CraterPort','Crater Port',''),(10,'MegaShip','Mega Ship','');
/*!40000 ALTER TABLE `ed_station_stationtype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_system_system`
--

LOCK TABLES `ed_system_system` WRITE;
/*!40000 ALTER TABLE `ed_system_system` DISABLE KEYS */;
INSERT INTO `ed_system_system` VALUES (1,'Synteini',51.78125,-76.40625,28.71875,'M',12756306529,'','2023-04-24 19:10:13.466297',5,NULL,NULL),(2,'Rhea',58.125,22.59375,-28.59375,'H',12958908273,'','2023-04-24 19:14:02.570660',5,NULL,NULL),(3,'Achenar',67.5,-119.46875,24.84375,'H',16380054761,'','2023-04-24 19:24:53.198203',2,NULL,NULL),(4,'Cemiess',66.0625,-105.34375,27.09375,'H',10000000000,'','2023-04-24 19:17:59.482152',2,NULL,NULL),(5,'Harma',-99.25,-100.96875,20.40625,'A',27790025,'','2023-04-24 19:24:09.542878',3,NULL,NULL),(6,'Eotienses',49.5,-104.03125,6.3125,'H',6467401235,'','2023-04-24 19:26:31.100696',5,NULL,NULL),(7,'Diso',72.15625,48.75,70.75,'M',4100025331,'','2023-04-24 19:27:34.603711',1,NULL,NULL),(8,'Sirius',6.25,-1.28125,-5.75,'H',2501068,'','2023-04-24 19:28:59.491641',3,NULL,NULL),(9,'Antal',-142.5,-91.375,-66.03125,'M',14826668,'','2023-04-24 19:30:09.717292',NULL,NULL,NULL),(10,'Euryale',35.375,-68.96875,24.8125,'M',640082,'','2023-04-24 19:31:20.944681',4,NULL,NULL),(11,'Sol',0,0,0,'H',22780919531,'','2023-04-24 19:32:48.461378',2,NULL,NULL);
/*!40000 ALTER TABLE `ed_system_system` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `eddn_datalog`
--

LOCK TABLES `eddn_datalog` WRITE;
/*!40000 ALTER TABLE `eddn_datalog` DISABLE KEYS */;
/*!40000 ALTER TABLE `eddn_datalog` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-24 22:55:44
