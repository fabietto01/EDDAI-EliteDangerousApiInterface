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

--
-- Dumping data for table `ed_bgs_minorfaction`
--

LOCK TABLES `ed_bgs_minorfaction` WRITE;
/*!40000 ALTER TABLE `ed_bgs_minorfaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `ed_bgs_minorfaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_bgs_minorfactioninsystem`
--

LOCK TABLES `ed_bgs_minorfactioninsystem` WRITE;
/*!40000 ALTER TABLE `ed_bgs_minorfactioninsystem` DISABLE KEYS */;
/*!40000 ALTER TABLE `ed_bgs_minorfactioninsystem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_bgs_power`
--

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
-- Dumping data for table `ed_bgs_stateinminorfaction`
--

LOCK TABLES `ed_bgs_stateinminorfaction` WRITE;
/*!40000 ALTER TABLE `ed_bgs_stateinminorfaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `ed_bgs_stateinminorfaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_body_atmospherecomponent`
--

LOCK TABLES `ed_body_atmospherecomponent` WRITE;
/*!40000 ALTER TABLE `ed_body_atmospherecomponent` DISABLE KEYS */;
INSERT INTO `ed_body_atmospherecomponent` VALUES (1,'Hydrogen','','Hydrogen'),(2,'Helium','','Helium'),(3,'Argon','','Argon'),(4,'Carbon Dioxide','','CarbonDioxide'),(5,'Nitrogen','','Nitrogen'),(6,'Silicates','','Silicates'),(7,'Iron','','Iron'),(8,'Methane','','Methane'),(9,'Oxygen','','Oxygen'),(10,'Sulphur Dioxide','','SulphurDioxide'),(11,'Neon','','Neon'),(12,'Water','','Water'),(13,'Ammonia','','Ammonia');
/*!40000 ALTER TABLE `ed_body_atmospherecomponent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_body_atmospherecomponentinplanet`
--

LOCK TABLES `ed_body_atmospherecomponentinplanet` WRITE;
/*!40000 ALTER TABLE `ed_body_atmospherecomponentinplanet` DISABLE KEYS */;
/*!40000 ALTER TABLE `ed_body_atmospherecomponentinplanet` ENABLE KEYS */;
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
-- Dumping data for table `ed_body_basebody`
--

LOCK TABLES `ed_body_basebody` WRITE;
/*!40000 ALTER TABLE `ed_body_basebody` DISABLE KEYS */;
/*!40000 ALTER TABLE `ed_body_basebody` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_body_materialinplanet`
--

LOCK TABLES `ed_body_materialinplanet` WRITE;
/*!40000 ALTER TABLE `ed_body_materialinplanet` DISABLE KEYS */;
/*!40000 ALTER TABLE `ed_body_materialinplanet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_body_planet`
--

LOCK TABLES `ed_body_planet` WRITE;
/*!40000 ALTER TABLE `ed_body_planet` DISABLE KEYS */;
/*!40000 ALTER TABLE `ed_body_planet` ENABLE KEYS */;
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
-- Dumping data for table `ed_body_ring`
--

LOCK TABLES `ed_body_ring` WRITE;
/*!40000 ALTER TABLE `ed_body_ring` DISABLE KEYS */;
/*!40000 ALTER TABLE `ed_body_ring` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_body_star`
--

LOCK TABLES `ed_body_star` WRITE;
/*!40000 ALTER TABLE `ed_body_star` DISABLE KEYS */;
/*!40000 ALTER TABLE `ed_body_star` ENABLE KEYS */;
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
/*!40000 ALTER TABLE `ed_economy_commodity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_economy_commodityinstation`
--

LOCK TABLES `ed_economy_commodityinstation` WRITE;
/*!40000 ALTER TABLE `ed_economy_commodityinstation` DISABLE KEYS */;
/*!40000 ALTER TABLE `ed_economy_commodityinstation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_economy_economy`
--

LOCK TABLES `ed_economy_economy` WRITE;
/*!40000 ALTER TABLE `ed_economy_economy` DISABLE KEYS */;
INSERT INTO `ed_economy_economy` VALUES (1,NULL,'Extraction',''),(2,NULL,'Refinery',''),(3,NULL,'Industrial',''),(4,'HighTech','High Tech',''),(5,'Agri','Agriculture',''),(6,NULL,'Terraforming',''),(7,NULL,'Tourism',''),(8,NULL,'Service',''),(9,NULL,'Military',''),(10,NULL,'Colony',''),(11,NULL,'Rescue',''),(12,NULL,'Damaged',''),(13,NULL,'Repair',''),(14,'PrivateEnterprise','Private Enterprise','');
/*!40000 ALTER TABLE `ed_economy_economy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_exploration_sample`
--

LOCK TABLES `ed_exploration_sample` WRITE;
/*!40000 ALTER TABLE `ed_exploration_sample` DISABLE KEYS */;
/*!40000 ALTER TABLE `ed_exploration_sample` ENABLE KEYS */;
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
-- Dumping data for table `ed_exploration_signal`
--

LOCK TABLES `ed_exploration_signal` WRITE;
/*!40000 ALTER TABLE `ed_exploration_signal` DISABLE KEYS */;
/*!40000 ALTER TABLE `ed_exploration_signal` ENABLE KEYS */;
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
-- Dumping data for table `ed_mining_hotspot`
--

LOCK TABLES `ed_mining_hotspot` WRITE;
/*!40000 ALTER TABLE `ed_mining_hotspot` DISABLE KEYS */;
/*!40000 ALTER TABLE `ed_mining_hotspot` ENABLE KEYS */;
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
/*!40000 ALTER TABLE `ed_station_service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_station_serviceinstation`
--

LOCK TABLES `ed_station_serviceinstation` WRITE;
/*!40000 ALTER TABLE `ed_station_serviceinstation` DISABLE KEYS */;
/*!40000 ALTER TABLE `ed_station_serviceinstation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_station_station`
--

LOCK TABLES `ed_station_station` WRITE;
/*!40000 ALTER TABLE `ed_station_station` DISABLE KEYS */;
/*!40000 ALTER TABLE `ed_station_station` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `ed_station_stationtype`
--

LOCK TABLES `ed_station_stationtype` WRITE;
/*!40000 ALTER TABLE `ed_station_stationtype` DISABLE KEYS */;
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
