mysqldump: [Warning] Using a password on the command line interface can be insecure.
-- MySQL dump 10.13  Distrib 8.4.0, for macos13.2 (arm64)
--
-- Host: localhost    Database: flytau
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Airports`
--

DROP TABLE IF EXISTS `Airports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Airports` (
  `airport_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `country` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `city` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`airport_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Airports`
--

LOCK TABLES `Airports` WRITE;
/*!40000 ALTER TABLE `Airports` DISABLE KEYS */;
INSERT INTO `Airports` (`airport_name`, `country`, `city`) VALUES ('AMS','Netherlands','Amsterdam'),('BER','Germany','Berlin'),('BKK','Thailand','Bangkok'),('CDG','France','Paris'),('DXB','UAE','Dubai'),('FCO','Italy','Rome'),('JFK','USA','New York'),('LHR','UK','London'),('NRT','Japan','Tokyo'),('TLV','Israel','Tel Aviv');
/*!40000 ALTER TABLE `Airports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Attendants`
--

DROP TABLE IF EXISTS `Attendants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Attendants` (
  `attendant_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name_he` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name_he` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone_number` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `city` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `street` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `house_number` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_work_date` date NOT NULL,
  `long_flight_certified` tinyint(1) NOT NULL,
  PRIMARY KEY (`attendant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Attendants`
--

LOCK TABLES `Attendants` WRITE;
/*!40000 ALTER TABLE `Attendants` DISABLE KEYS */;
INSERT INTO `Attendants` (`attendant_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('100000001','נועה','קירל','054-1000001','Tel Aviv','HaYarkon','1','2022-01-01',1),('100000002','אנה','זק','054-1000002','Ashdod','HaYam','2','2022-01-02',1),('100000003','יונתן','מרגי','054-1000003','Yehud','HaAtzmaut','3','2022-01-03',0),('100000004','סטטיק','רוסו','054-1000004','Haifa','Moriah','4','2022-01-04',1),('100000005','בן','תבורי','054-1000005','Tel Aviv','Dizengoff','5','2022-01-05',0),('100000006','אגס','קימל','054-1000006','Tel Aviv','Rothschild','6','2022-01-06',0),('100000007','עדן','בן זקן','054-1000007','Kiryat Shmona','HaHagana','7','2022-01-07',1),('100000008','נטע','ברזילי','054-1000008','Hod HaSharon','HaBanim','8','2022-01-08',1),('100000009','רן','דנקר','054-1000009','Tel Aviv','Shenkin','9','2022-01-09',1),('100000010','עברי','לידר','054-1000010','Tel Aviv','Melchet','10','2022-01-10',1),('100000011','הראל','סקעת','054-1000011','Kfar Saba','HaKikar','11','2022-01-11',0),('100000012','שירי','מימון','054-1000012','Haifa','HaNassi','12','2022-01-12',1),('100000013','נינט','טייב','054-1000013','Kiryat Gat','Lachish','13','2022-01-13',1),('100000014','אביב','גפן','054-1000014','Tzahala','HaMishtala','14','2022-01-14',0),('100000015','אייל','גולן','054-1000015','Rehovot','Herzl','15','2022-01-15',1),('100000016','משה','פרץ','054-1000016','Tiberias','HaGalil','16','2022-01-16',0),('100000017','עומר','אדם','054-1000017','Mishmar HaShiva','HaZayit','17','2022-01-17',1),('100000018','דודו','אהרון','054-1000018','Ekron','HaRimon','18','2022-01-18',0),('100000019','קובי','פרץ','054-1000019','Tel Aviv','HaYarkon','19','2022-01-19',1),('100000020','שרית','חדד','054-1000020','Hadera','HaNassi','20','2022-01-20',1),('100000021','עדן','חסון','054-1000021','Pardes Hanna','HaDekel','21','2023-01-21',1),('100000022','חנן','בן ארי','054-1000022','Pardes Hanna','HaOren','22','2023-02-22',1),('100000023','ישי','ריבו','054-1000023','Jerusalem','Jaffa','23','2023-03-23',0),('100000024','יסמין','מועלם','054-1000024','Tel Aviv','Florentin','24','2023-04-24',1),('100000025','איתי','זבולון','054-1000025','Tel Aviv','Kaplan','25','2023-05-25',0),('100000026','רוני','דלומי','054-1000026','Givataim','Katznelson','26','2023-06-26',1),('100000027','אליעד','נחום','054-1000027','Bat Yam','HaAtzmaut','27','2023-07-27',1),('100000028','מירי','מסיקה','054-1000028','Ono','Levi Eshkol','28','2023-08-28',1),('100000029','סטפן','לגר','054-1000029','Bat Yam','Yoseftal','29','2023-09-29',1),('100000030','ואלרי','חמאתי','054-1000030','Jaffa','Yefet','30','2023-10-30',0),('100000031','רביב','כנר','054-1000031','Holon','Eilat','31','2023-11-05',1),('100000032','אלה לי','להב','054-1000032','Shoham','HaTamar','32','2023-11-10',0),('100000033','תמיר','גרינברג','054-1000033','Tel Aviv','Allenby','33','2023-12-01',1),('100000034','נרקיס','ראובן-נגר','054-1000034','Ashkelon','Bar Kokhba','34','2024-01-15',1),('100000035','נונו','גרין','054-1000035','Tel Aviv','King George','35','2024-02-20',0);
/*!40000 ALTER TABLE `Attendants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Attendants_In_Flights`
--

DROP TABLE IF EXISTS `Attendants_In_Flights`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Attendants_In_Flights` (
  `attendant_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `flight_id` int NOT NULL,
  PRIMARY KEY (`attendant_id`,`flight_id`),
  KEY `flight_id` (`flight_id`),
  CONSTRAINT `attendants_in_flights_ibfk_1` FOREIGN KEY (`attendant_id`) REFERENCES `Attendants` (`attendant_id`),
  CONSTRAINT `attendants_in_flights_ibfk_2` FOREIGN KEY (`flight_id`) REFERENCES `Flights` (`flight_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Attendants_In_Flights`
--

LOCK TABLES `Attendants_In_Flights` WRITE;
/*!40000 ALTER TABLE `Attendants_In_Flights` DISABLE KEYS */;
INSERT INTO `Attendants_In_Flights` (`attendant_id`, `flight_id`) VALUES ('100000009',1005),('100000010',1005),('100000012',1005),('100000013',1005),('100000015',1005),('100000017',1005),('100000001',1006),('100000002',1006),('100000004',1006),('100000007',1006),('100000008',1006),('100000019',1006),('100000003',1007),('100000005',1007),('100000016',1007),('100000001',3001),('100000002',3001),('100000003',3001),('100000004',3001),('100000005',3001),('100000006',3001),('100000007',3002),('100000008',3002),('100000009',3002),('100000010',3002),('100000011',3002),('100000012',3002),('100000013',3003),('100000014',3003),('100000015',3003),('100000016',3003),('100000017',3003),('100000018',3003),('100000001',3005),('100000019',3005),('100000020',3005),('100000002',3007),('100000003',3007),('100000004',3007),('100000005',3009),('100000006',3009),('100000007',3009);
/*!40000 ALTER TABLE `Attendants_In_Flights` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `FlightRoutes`
--

DROP TABLE IF EXISTS `FlightRoutes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `FlightRoutes` (
  `origin_airport_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `destination_airport_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `flight_duration` int NOT NULL,
  PRIMARY KEY (`origin_airport_name`,`destination_airport_name`),
  KEY `destination_airport_name` (`destination_airport_name`),
  CONSTRAINT `flightroutes_ibfk_1` FOREIGN KEY (`origin_airport_name`) REFERENCES `Airports` (`airport_name`),
  CONSTRAINT `flightroutes_ibfk_2` FOREIGN KEY (`destination_airport_name`) REFERENCES `Airports` (`airport_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FlightRoutes`
--

LOCK TABLES `FlightRoutes` WRITE;
/*!40000 ALTER TABLE `FlightRoutes` DISABLE KEYS */;
INSERT INTO `FlightRoutes` (`origin_airport_name`, `destination_airport_name`, `flight_duration`) VALUES ('AMS','BER',80),('AMS','BKK',660),('AMS','CDG',90),('AMS','DXB',400),('AMS','FCO',135),('AMS','JFK',485),('AMS','LHR',70),('AMS','NRT',780),('AMS','TLV',290),('BER','AMS',85),('BER','BKK',650),('BER','CDG',110),('BER','DXB',380),('BER','FCO',120),('BER','JFK',515),('BER','LHR',115),('BER','NRT',770),('BER','TLV',240),('BKK','AMS',720),('BKK','BER',710),('BKK','CDG',730),('BKK','DXB',410),('BKK','FCO',700),('BKK','JFK',1020),('BKK','LHR',750),('BKK','NRT',360),('BKK','TLV',690),('CDG','AMS',85),('CDG','BER',105),('CDG','BKK',670),('CDG','DXB',400),('CDG','FCO',125),('CDG','JFK',475),('CDG','LHR',80),('CDG','NRT',790),('CDG','TLV',270),('DXB','AMS',430),('DXB','BER',410),('DXB','BKK',380),('DXB','CDG',430),('DXB','FCO',380),('DXB','JFK',820),('DXB','LHR',450),('DXB','NRT',580),('DXB','TLV',215),('FCO','AMS',140),('FCO','BER',125),('FCO','BKK',640),('FCO','CDG',130),('FCO','DXB',350),('FCO','JFK',540),('FCO','LHR',160),('FCO','NRT',800),('FCO','TLV',220),('JFK','AMS',460),('JFK','BER',490),('JFK','BKK',1080),('JFK','CDG',450),('JFK','DXB',760),('JFK','FCO',510),('JFK','LHR',420),('JFK','NRT',840),('JFK','TLV',660),('LHR','AMS',65),('LHR','BER',110),('LHR','BKK',690),('LHR','CDG',75),('LHR','DXB',420),('LHR','FCO',155),('LHR','JFK',445),('LHR','NRT',810),('LHR','TLV',300),('NRT','AMS',830),('NRT','BER',820),('NRT','BKK',400),('NRT','CDG',840),('NRT','DXB',620),('NRT','FCO',850),('NRT','JFK',780),('NRT','LHR',860),('NRT','TLV',780),('TLV','AMS',300),('TLV','BER',250),('TLV','BKK',660),('TLV','CDG',280),('TLV','DXB',210),('TLV','FCO',230),('TLV','JFK',720),('TLV','LHR',300),('TLV','NRT',750);
/*!40000 ALTER TABLE `FlightRoutes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Flights`
--

DROP TABLE IF EXISTS `Flights`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Flights` (
  `flight_id` int NOT NULL,
  `departure_time` time NOT NULL,
  `departure_date` date NOT NULL,
  `status` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `plane_id` int NOT NULL,
  `origin_airport_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `destination_airport_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `price_economy` decimal(10,2) NOT NULL DEFAULT '0.00',
  `price_business` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`flight_id`),
  KEY `plane_id` (`plane_id`),
  KEY `origin_airport_name` (`origin_airport_name`,`destination_airport_name`),
  CONSTRAINT `flights_ibfk_1` FOREIGN KEY (`plane_id`) REFERENCES `Planes` (`plane_id`),
  CONSTRAINT `flights_ibfk_2` FOREIGN KEY (`origin_airport_name`, `destination_airport_name`) REFERENCES `FlightRoutes` (`origin_airport_name`, `destination_airport_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Flights`
--

LOCK TABLES `Flights` WRITE;
/*!40000 ALTER TABLE `Flights` DISABLE KEYS */;
INSERT INTO `Flights` (`flight_id`, `departure_time`, `departure_date`, `status`, `plane_id`, `origin_airport_name`, `destination_airport_name`, `price_economy`, `price_business`) VALUES (1001,'08:00:00','2026-06-01','Active',1,'TLV','JFK',600.00,1200.00),(1002,'14:00:00','2026-06-02','Cancelled',2,'TLV','LHR',300.00,NULL),(1003,'10:00:00','2026-07-10','Active',3,'CDG','TLV',550.00,1100.00),(1004,'23:00:00','2026-08-15','Active',1,'JFK','TLV',700.00,1500.00),(1005,'20:15:00','2026-06-15','Cancelled',1,'TLV','JFK',400.00,1000.00),(1006,'20:20:00','2026-06-15','Active',5,'JFK','TLV',32.00,432.00),(1007,'20:00:00','2026-06-15','Active',4,'CDG','TLV',800.00,NULL),(1044,'08:00:00','2026-06-01','Active',1,'TLV','NRT',670.00,1230.00),(3001,'23:55:00','2024-05-01','Landed',1,'TLV','JFK',800.00,1600.00),(3002,'12:00:00','2024-06-15','Landed',3,'TLV','NRT',1100.00,2200.00),(3003,'01:00:00','2026-11-20','Active',5,'TLV','BKK',750.00,1500.00),(3004,'15:00:00','2024-08-10','Cancelled',1,'JFK','TLV',850.00,1700.00),(3005,'08:00:00','2024-04-10','Landed',2,'TLV','LHR',400.00,NULL),(3006,'16:30:00','2024-04-12','Landed',2,'LHR','TLV',400.00,NULL),(3007,'09:00:00','2024-07-20','Landed',4,'TLV','CDG',350.00,NULL),(3008,'18:00:00','2024-07-25','Landed',4,'CDG','TLV',350.00,NULL),(3009,'07:00:00','2026-12-01','Active',6,'TLV','FCO',300.00,NULL),(3010,'14:00:00','2026-12-05','Active',6,'FCO','TLV',300.00,NULL),(3011,'10:00:00','2026-10-10','Active',4,'TLV','AMS',450.00,NULL),(3012,'13:00:00','2024-09-01','Cancelled',2,'TLV','BER',320.00,NULL),(3033,'23:55:00','2024-08-01','Landed',5,'DXB','JFK',900.00,1650.00),(3034,'22:55:00','2026-01-23','Active',1,'BKK','DXB',700.00,1200.00);
/*!40000 ALTER TABLE `Flights` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `FlightTickets`
--

DROP TABLE IF EXISTS `FlightTickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `FlightTickets` (
  `order_id` int NOT NULL,
  `flight_id` int NOT NULL,
  `plane_id` int NOT NULL,
  `seat_row` int NOT NULL,
  `seat_column` int NOT NULL,
  PRIMARY KEY (`order_id`,`flight_id`,`plane_id`,`seat_row`,`seat_column`),
  KEY `flight_id` (`flight_id`),
  KEY `plane_id` (`plane_id`,`seat_row`,`seat_column`),
  CONSTRAINT `flighttickets_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `Orders` (`order_id`),
  CONSTRAINT `flighttickets_ibfk_2` FOREIGN KEY (`flight_id`) REFERENCES `Flights` (`flight_id`),
  CONSTRAINT `flighttickets_ibfk_3` FOREIGN KEY (`plane_id`, `seat_row`, `seat_column`) REFERENCES `Seats` (`plane_id`, `seat_row`, `seat_column`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FlightTickets`
--

LOCK TABLES `FlightTickets` WRITE;
/*!40000 ALTER TABLE `FlightTickets` DISABLE KEYS */;
INSERT INTO `FlightTickets` (`order_id`, `flight_id`, `plane_id`, `seat_row`, `seat_column`) VALUES (501,1001,1,1,1),(502,1001,1,1,2),(511,1001,1,15,4),(511,1001,1,15,5),(511,1001,1,15,6),(503,1002,2,1,1),(504,1002,2,1,2),(505,1002,2,1,5),(505,1002,2,1,6),(506,1002,2,1,3),(506,1002,2,1,4),(508,1003,3,2,4),(7006,1006,5,1,1),(7006,1006,5,1,2),(8007,1044,1,11,4),(8007,1044,1,11,5),(8007,1044,1,11,6),(7001,3001,1,2,2),(7002,3001,1,12,1),(7002,3001,1,12,2),(7003,3002,3,15,5),(7007,3003,5,11,1),(7007,3003,5,11,2),(7004,3005,2,5,1),(7004,3005,2,5,2),(7004,3005,2,5,3),(8006,3009,6,4,1),(8006,3009,6,4,2),(8008,3034,1,10,1),(8008,3034,1,10,2),(8008,3034,1,10,3);
/*!40000 ALTER TABLE `FlightTickets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Guests`
--

DROP TABLE IF EXISTS `Guests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Guests` (
  `UserEmail` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`UserEmail`),
  CONSTRAINT `guests_ibfk_1` FOREIGN KEY (`UserEmail`) REFERENCES `Users` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Guests`
--

LOCK TABLES `Guests` WRITE;
/*!40000 ALTER TABLE `Guests` DISABLE KEYS */;
INSERT INTO `Guests` (`UserEmail`) VALUES ('gabi@gmail.com'),('guest1@temp.com'),('guest2@temp.com'),('ortalleviron@mail.tau.ac.il');
/*!40000 ALTER TABLE `Guests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Managers`
--

DROP TABLE IF EXISTS `Managers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Managers` (
  `manager_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name_he` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name_he` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone_number` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `city` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `street` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `house_number` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_work_date` date NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`manager_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Managers`
--

LOCK TABLES `Managers` WRITE;
/*!40000 ALTER TABLE `Managers` DISABLE KEYS */;
INSERT INTO `Managers` (`manager_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `password`) VALUES ('300000001','מנהל','ראשי','050-1111111','Tel Aviv','Rothschild','10','2015-01-01','admin123'),('300000002','מנהל','משני','050-2222222','Haifa','Herzl','5','2018-06-01','admin456');
/*!40000 ALTER TABLE `Managers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Orders`
--

DROP TABLE IF EXISTS `Orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Orders` (
  `order_id` int NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `order_status` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `order_date` date NOT NULL,
  `total_payment` decimal(10,2) NOT NULL,
  PRIMARY KEY (`order_id`),
  KEY `email` (`email`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`email`) REFERENCES `Users` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Orders`
--

LOCK TABLES `Orders` WRITE;
/*!40000 ALTER TABLE `Orders` DISABLE KEYS */;
INSERT INTO `Orders` (`order_id`, `email`, `order_status`, `order_date`, `total_payment`) VALUES (501,'reg1@gmail.com','Confirmed','2026-01-10',1200.00),(502,'guest1@temp.com','Confirmed','2026-01-12',1200.00),(503,'reg2@yahoo.com','Cancelled by System','2026-02-05',0.00),(504,'guest2@temp.com','Cancelled by System','2026-03-20',0.00),(505,'lihibarmeir@mail.tau.ac.il','Cancelled by System','2026-01-07',0.00),(506,'lihibarmeir@mail.tau.ac.il','Cancelled by System','2026-01-07',0.00),(507,'lihibarmeir@mail.tau.ac.il','Cancelled by Customer','2026-01-07',2400.00),(508,'ortalleviron@mail.tau.ac.il','Confirmed','2026-01-07',1100.00),(509,'lihibarmeir@mail.tau.ac.il','Cancelled by Customer','2026-01-07',2400.00),(510,'ortalleviron@mail.tau.ac.il','Cancelled by Customer','2026-01-07',600.00),(511,'noyastorzi@mail.tau.ac.il','Active','2026-01-07',1800.00),(7001,'reg1@gmail.com','Confirmed','2024-04-15',1600.00),(7002,'guest1@temp.com','Confirmed','2024-04-20',1600.00),(7003,'reg2@yahoo.com','Confirmed','2024-05-01',1100.00),(7004,'guest2@temp.com','Confirmed','2024-03-01',1200.00),(7005,'lihibarmeir@mail.tau.ac.il','Cancelled','2026-01-14',1600.00),(7006,'lihibarmeir@mail.tau.ac.il','Active','2026-01-14',864.00),(7007,'lihibarmeir@mail.tau.ac.il','Active','2026-01-14',1500.00),(8001,'reg1@gmail.com','Cancelled','2024-04-18',1600.00),(8002,'guest1@temp.com','Cancelled','2024-04-22',400.00),(8003,'reg2@yahoo.com','Cancelled','2024-05-10',1100.00),(8004,'guest2@temp.com','Cancelled','2026-11-01',900.00),(8005,'lihibarmeir@mail.tau.ac.il','Cancelled','2026-04-05',950.00),(8006,'lihibarmeir@mail.tau.ac.il','Active','2026-01-18',600.00),(8007,'lihibarmeir@mail.tau.ac.il','Active','2026-01-22',2010.00),(8008,'lihibarmeir@mail.tau.ac.il','Active','2026-01-22',2100.00);
/*!40000 ALTER TABLE `Orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Pilots`
--

DROP TABLE IF EXISTS `Pilots`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Pilots` (
  `pilot_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name_he` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name_he` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone_number` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `city` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `street` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `house_number` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_work_date` date NOT NULL,
  `long_flight_certified` tinyint(1) NOT NULL,
  PRIMARY KEY (`pilot_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pilots`
--

LOCK TABLES `Pilots` WRITE;
/*!40000 ALTER TABLE `Pilots` DISABLE KEYS */;
INSERT INTO `Pilots` (`pilot_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('12345678','ביבי','נתניהו','0528638618','caesarea','schoona 13','15','2026-01-22',1),('200000001','ישראל','ישראלי','052-1000001','Ramat Gan','HaRoeh','1','2019-01-01',1),('200000002','דוד','כהן','052-1000002','Givatayim','Weizmann','2','2019-02-01',1),('200000003','משה','לוי','052-1000003','Holon','Sokolov','3','2020-03-01',0),('200000004','יעקב','אברהם','052-1000004','Bat Yam','Jerusalem','4','2020-04-01',1),('200000005','יצחק','רבין','052-1000005','Rishon LeZion','Jabotinsky','5','2021-05-01',0),('200000006','חיים','נחמן','052-1000006','Petah Tikva','HaHistadrut','6','2021-06-01',1),('200000007','שאול','מופז','052-1000007','Netanya','Herzl','7','2022-07-01',0),('200000008','אהוד','ברק','052-1000008','Herzliya','HaBanim','8','2022-08-01',1),('200000009','אריאל','שרון','052-1000009','Kfar Saba','Weizmann','9','2023-09-01',0),('200000010','מנחם','בגין','052-1000010','Ra\'anana','Ahuza','10','2023-10-01',1),('200000011','שמעון','פרס','052-1000011','Tel Aviv','HaShalom','11','2023-11-01',1),('200000012','גולדה','מאיר','052-1000012','Jerusalem','Balfour','12','2023-12-01',0),('200000013','עזר','ויצמן','052-1000013','Caesarea','HaHof','13','2024-01-01',1),('200000014','בני','גנץ','052-1000014','Rosh HaAyin','Nofar','14','2024-02-01',1),('200000015','יאיר','לפיד','052-1000015','Tel Aviv','Eisenberg','15','2024-03-01',0),('200000016','משה','דיין','052-1000016','Nahalal','HaEmek','16','2024-04-01',1),('200000017','נפתלי','בנט','052-1000017','Ra\'anana','Keren HaYesod','17','2024-05-01',0),('200000018','ראובן','ריבלין','052-1000018','Jerusalem','HaNassi','18','2024-06-01',1);
/*!40000 ALTER TABLE `Pilots` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Pilots_In_Flights`
--

DROP TABLE IF EXISTS `Pilots_In_Flights`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Pilots_In_Flights` (
  `pilot_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `flight_id` int NOT NULL,
  PRIMARY KEY (`pilot_id`,`flight_id`),
  KEY `flight_id` (`flight_id`),
  CONSTRAINT `pilots_in_flights_ibfk_1` FOREIGN KEY (`pilot_id`) REFERENCES `Pilots` (`pilot_id`),
  CONSTRAINT `pilots_in_flights_ibfk_2` FOREIGN KEY (`flight_id`) REFERENCES `Flights` (`flight_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pilots_In_Flights`
--

LOCK TABLES `Pilots_In_Flights` WRITE;
/*!40000 ALTER TABLE `Pilots_In_Flights` DISABLE KEYS */;
INSERT INTO `Pilots_In_Flights` (`pilot_id`, `flight_id`) VALUES ('200000006',1005),('200000008',1005),('200000010',1005),('200000001',1006),('200000002',1006),('200000004',1006),('200000007',1007),('200000009',1007),('200000001',3001),('200000002',3001),('200000008',3001),('200000004',3002),('200000006',3002),('200000010',3002),('200000001',3003),('200000002',3003),('200000008',3003),('200000003',3005),('200000005',3005),('200000007',3007),('200000009',3007),('200000003',3009),('200000005',3009);
/*!40000 ALTER TABLE `Pilots_In_Flights` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Planes`
--

DROP TABLE IF EXISTS `Planes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Planes` (
  `plane_id` int NOT NULL,
  `manufacturer` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `size` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `purchase_date` date NOT NULL,
  PRIMARY KEY (`plane_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Planes`
--

LOCK TABLES `Planes` WRITE;
/*!40000 ALTER TABLE `Planes` DISABLE KEYS */;
INSERT INTO `Planes` (`plane_id`, `manufacturer`, `size`, `purchase_date`) VALUES (1,'Boeing','Large','2020-01-01'),(2,'Boeing','Small','2021-05-15'),(3,'Airbus','Large','2019-11-20'),(4,'Airbus','Small','2022-03-10'),(5,'Boeing','Large','2018-08-08'),(6,'Dassault','Small','2023-01-01'),(7,'Dassault','Small','2026-01-22'),(10034,'Boeing','Large','2026-01-20');
/*!40000 ALTER TABLE `Planes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `RegisteredUsers`
--

DROP TABLE IF EXISTS `RegisteredUsers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `RegisteredUsers` (
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `passport_number` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `birth_date` date NOT NULL,
  `registration_date` date NOT NULL,
  PRIMARY KEY (`email`),
  CONSTRAINT `registeredusers_ibfk_1` FOREIGN KEY (`email`) REFERENCES `Users` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RegisteredUsers`
--

LOCK TABLES `RegisteredUsers` WRITE;
/*!40000 ALTER TABLE `RegisteredUsers` DISABLE KEYS */;
INSERT INTO `RegisteredUsers` (`email`, `password`, `passport_number`, `birth_date`, `registration_date`) VALUES ('lihibarmeir@mail.tau.ac.il','lihi1234','3245876938','2026-01-06','2026-01-07'),('noyastorzi@mail.tau.ac.il','n12345!','207891466','2000-12-30','2026-01-07'),('reg1@gmail.com','pass123','P100200300','1990-05-15','2024-01-01'),('reg2@yahoo.com','pass456','P400500600','1995-08-20','2024-02-10');
/*!40000 ALTER TABLE `RegisteredUsers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Seats`
--

DROP TABLE IF EXISTS `Seats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Seats` (
  `plane_id` int NOT NULL,
  `seat_row` int NOT NULL,
  `seat_column` int NOT NULL,
  `seat_class` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`plane_id`,`seat_row`,`seat_column`),
  CONSTRAINT `seats_ibfk_1` FOREIGN KEY (`plane_id`) REFERENCES `Planes` (`plane_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Seats`
--

LOCK TABLES `Seats` WRITE;
/*!40000 ALTER TABLE `Seats` DISABLE KEYS */;
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1,1,1,'Business'),(1,1,2,'Business'),(1,1,3,'Business'),(1,1,4,'Business'),(1,2,1,'Business'),(1,2,2,'Business'),(1,2,3,'Business'),(1,2,4,'Business'),(1,3,1,'Business'),(1,3,2,'Business'),(1,3,3,'Business'),(1,3,4,'Business'),(1,4,1,'Business'),(1,4,2,'Business'),(1,4,3,'Business'),(1,4,4,'Business'),(1,10,1,'Economy'),(1,10,2,'Economy'),(1,10,3,'Economy'),(1,10,4,'Economy'),(1,10,5,'Economy'),(1,10,6,'Economy'),(1,11,1,'Economy'),(1,11,2,'Economy'),(1,11,3,'Economy'),(1,11,4,'Economy'),(1,11,5,'Economy'),(1,11,6,'Economy'),(1,12,1,'Economy'),(1,12,2,'Economy'),(1,12,3,'Economy'),(1,12,4,'Economy'),(1,12,5,'Economy'),(1,12,6,'Economy'),(1,13,1,'Economy'),(1,13,2,'Economy'),(1,13,3,'Economy'),(1,13,4,'Economy'),(1,13,5,'Economy'),(1,13,6,'Economy'),(1,14,1,'Economy'),(1,14,2,'Economy'),(1,14,3,'Economy'),(1,14,4,'Economy'),(1,14,5,'Economy'),(1,14,6,'Economy'),(1,15,1,'Economy'),(1,15,2,'Economy'),(1,15,3,'Economy'),(1,15,4,'Economy'),(1,15,5,'Economy'),(1,15,6,'Economy'),(1,16,1,'Economy'),(1,16,2,'Economy'),(1,16,3,'Economy'),(1,16,4,'Economy'),(1,16,5,'Economy'),(1,16,6,'Economy'),(1,17,1,'Economy'),(1,17,2,'Economy'),(1,17,3,'Economy'),(1,17,4,'Economy'),(1,17,5,'Economy'),(1,17,6,'Economy'),(1,18,1,'Economy'),(1,18,2,'Economy'),(1,18,3,'Economy'),(1,18,4,'Economy'),(1,18,5,'Economy'),(1,18,6,'Economy'),(1,19,1,'Economy'),(1,19,2,'Economy'),(1,19,3,'Economy'),(1,19,4,'Economy'),(1,19,5,'Economy'),(1,19,6,'Economy'),(1,20,1,'Economy'),(1,20,2,'Economy'),(1,20,3,'Economy'),(1,20,4,'Economy'),(1,20,5,'Economy'),(1,20,6,'Economy'),(2,1,1,'Economy'),(2,1,2,'Economy'),(2,1,3,'Economy'),(2,1,4,'Economy'),(2,1,5,'Economy'),(2,1,6,'Economy'),(2,2,1,'Economy'),(2,2,2,'Economy'),(2,2,3,'Economy'),(2,2,4,'Economy'),(2,2,5,'Economy'),(2,2,6,'Economy'),(2,3,1,'Economy'),(2,3,2,'Economy'),(2,3,3,'Economy'),(2,3,4,'Economy'),(2,3,5,'Economy'),(2,3,6,'Economy'),(2,4,1,'Economy'),(2,4,2,'Economy'),(2,4,3,'Economy'),(2,4,4,'Economy'),(2,4,5,'Economy'),(2,4,6,'Economy'),(2,5,1,'Economy'),(2,5,2,'Economy'),(2,5,3,'Economy'),(2,5,4,'Economy'),(2,5,5,'Economy'),(2,5,6,'Economy'),(2,6,1,'Economy'),(2,6,2,'Economy'),(2,6,3,'Economy'),(2,6,4,'Economy'),(2,6,5,'Economy'),(2,6,6,'Economy'),(2,7,1,'Economy'),(2,7,2,'Economy'),(2,7,3,'Economy'),(2,7,4,'Economy'),(2,7,5,'Economy'),(2,7,6,'Economy'),(2,8,1,'Economy'),(2,8,2,'Economy'),(2,8,3,'Economy'),(2,8,4,'Economy'),(2,8,5,'Economy'),(2,8,6,'Economy'),(2,9,1,'Economy'),(2,9,2,'Economy'),(2,9,3,'Economy'),(2,9,4,'Economy'),(2,9,5,'Economy'),(2,9,6,'Economy'),(2,10,1,'Economy'),(2,10,2,'Economy'),(2,10,3,'Economy'),(2,10,4,'Economy'),(2,10,5,'Economy'),(2,10,6,'Economy'),(2,11,1,'Economy'),(2,11,2,'Economy'),(2,11,3,'Economy'),(2,11,4,'Economy'),(2,11,5,'Economy'),(2,11,6,'Economy'),(2,12,1,'Economy'),(2,12,2,'Economy'),(2,12,3,'Economy'),(2,12,4,'Economy'),(2,12,5,'Economy'),(2,12,6,'Economy'),(2,13,1,'Economy'),(2,13,2,'Economy'),(2,13,3,'Economy'),(2,13,4,'Economy'),(2,13,5,'Economy'),(2,13,6,'Economy'),(2,14,1,'Economy'),(2,14,2,'Economy'),(2,14,3,'Economy'),(2,14,4,'Economy'),(2,14,5,'Economy'),(2,14,6,'Economy'),(2,15,1,'Economy'),(2,15,2,'Economy'),(2,15,3,'Economy'),(2,15,4,'Economy'),(2,15,5,'Economy'),(2,15,6,'Economy'),(3,1,1,'Business'),(3,1,2,'Business'),(3,1,3,'Business'),(3,1,4,'Business'),(3,2,1,'Business'),(3,2,2,'Business'),(3,2,3,'Business'),(3,2,4,'Business'),(3,10,1,'Economy'),(3,10,2,'Economy'),(3,10,3,'Economy'),(3,10,4,'Economy'),(3,10,5,'Economy'),(3,10,6,'Economy'),(3,11,1,'Economy'),(3,11,2,'Economy'),(3,11,3,'Economy'),(3,11,4,'Economy'),(3,11,5,'Economy'),(3,11,6,'Economy'),(3,12,1,'Economy'),(3,12,2,'Economy'),(3,12,3,'Economy'),(3,12,4,'Economy'),(3,12,5,'Economy'),(3,12,6,'Economy'),(3,13,1,'Economy'),(3,13,2,'Economy'),(3,13,3,'Economy'),(3,13,4,'Economy'),(3,13,5,'Economy'),(3,13,6,'Economy'),(3,14,1,'Economy'),(3,14,2,'Economy'),(3,14,3,'Economy'),(3,14,4,'Economy'),(3,14,5,'Economy'),(3,14,6,'Economy'),(3,15,1,'Economy'),(3,15,2,'Economy'),(3,15,3,'Economy'),(3,15,4,'Economy'),(3,15,5,'Economy'),(3,15,6,'Economy'),(4,1,1,'Economy'),(4,1,2,'Economy'),(4,1,3,'Economy'),(4,1,4,'Economy'),(4,1,5,'Economy'),(4,1,6,'Economy'),(4,2,1,'Economy'),(4,2,2,'Economy'),(4,2,3,'Economy'),(4,2,4,'Economy'),(4,2,5,'Economy'),(4,2,6,'Economy'),(4,3,1,'Economy'),(4,3,2,'Economy'),(4,3,3,'Economy'),(4,3,4,'Economy'),(4,3,5,'Economy'),(4,3,6,'Economy'),(4,4,1,'Economy'),(4,4,2,'Economy'),(4,4,3,'Economy'),(4,4,4,'Economy'),(4,4,5,'Economy'),(4,4,6,'Economy'),(4,5,1,'Economy'),(4,5,2,'Economy'),(4,5,3,'Economy'),(4,5,4,'Economy'),(4,5,5,'Economy'),(4,5,6,'Economy'),(4,6,1,'Economy'),(4,6,2,'Economy'),(4,6,3,'Economy'),(4,6,4,'Economy'),(4,6,5,'Economy'),(4,6,6,'Economy'),(4,7,1,'Economy'),(4,7,2,'Economy'),(4,7,3,'Economy'),(4,7,4,'Economy'),(4,7,5,'Economy'),(4,7,6,'Economy'),(4,8,1,'Economy'),(4,8,2,'Economy'),(4,8,3,'Economy'),(4,8,4,'Economy'),(4,8,5,'Economy'),(4,8,6,'Economy'),(4,9,1,'Economy'),(4,9,2,'Economy'),(4,9,3,'Economy'),(4,9,4,'Economy'),(4,9,5,'Economy'),(4,9,6,'Economy'),(4,10,1,'Economy'),(4,10,2,'Economy'),(4,10,3,'Economy'),(4,10,4,'Economy'),(4,10,5,'Economy'),(4,10,6,'Economy'),(5,1,1,'Business'),(5,1,2,'Business'),(5,1,3,'Business'),(5,1,4,'Business'),(5,10,1,'Economy'),(5,10,2,'Economy'),(5,10,3,'Economy'),(5,10,4,'Economy'),(5,10,5,'Economy'),(5,10,6,'Economy'),(5,11,1,'Economy'),(5,11,2,'Economy'),(5,11,3,'Economy'),(5,11,4,'Economy'),(5,11,5,'Economy'),(5,11,6,'Economy'),(5,12,1,'Economy'),(5,12,2,'Economy'),(5,12,3,'Economy'),(5,12,4,'Economy'),(5,12,5,'Economy'),(5,12,6,'Economy'),(6,1,1,'Economy'),(6,1,2,'Economy'),(6,1,3,'Economy'),(6,1,4,'Economy'),(6,2,1,'Economy'),(6,2,2,'Economy'),(6,2,3,'Economy'),(6,2,4,'Economy'),(6,3,1,'Economy'),(6,3,2,'Economy'),(6,3,3,'Economy'),(6,3,4,'Economy'),(6,4,1,'Economy'),(6,4,2,'Economy'),(6,4,3,'Economy'),(6,4,4,'Economy'),(6,5,1,'Economy'),(6,5,2,'Economy'),(6,5,3,'Economy'),(6,5,4,'Economy'),(6,6,1,'Economy'),(6,6,2,'Economy'),(6,6,3,'Economy'),(6,6,4,'Economy'),(6,7,1,'Economy'),(6,7,2,'Economy'),(6,7,3,'Economy'),(6,7,4,'Economy'),(6,8,1,'Economy'),(6,8,2,'Economy'),(6,8,3,'Economy'),(6,8,4,'Economy'),(6,9,1,'Economy'),(6,9,2,'Economy'),(6,9,3,'Economy'),(6,9,4,'Economy'),(6,10,1,'Economy'),(6,10,2,'Economy'),(6,10,3,'Economy'),(6,10,4,'Economy'),(7,1,1,'Economy'),(7,1,2,'Economy'),(7,1,3,'Economy'),(7,1,4,'Economy'),(7,1,5,'Economy'),(7,1,6,'Economy'),(7,2,1,'Economy'),(7,2,2,'Economy'),(7,2,3,'Economy'),(7,2,4,'Economy'),(7,2,5,'Economy'),(7,2,6,'Economy'),(7,3,1,'Economy'),(7,3,2,'Economy'),(7,3,3,'Economy'),(7,3,4,'Economy'),(7,3,5,'Economy'),(7,3,6,'Economy'),(7,4,1,'Economy'),(7,4,2,'Economy'),(7,4,3,'Economy'),(7,4,4,'Economy'),(7,4,5,'Economy'),(7,4,6,'Economy'),(7,5,1,'Economy'),(7,5,2,'Economy'),(7,5,3,'Economy'),(7,5,4,'Economy'),(7,5,5,'Economy'),(7,5,6,'Economy'),(7,6,1,'Economy'),(7,6,2,'Economy'),(7,6,3,'Economy'),(7,6,4,'Economy'),(7,6,5,'Economy'),(7,6,6,'Economy'),(7,7,1,'Economy'),(7,7,2,'Economy'),(7,7,3,'Economy'),(7,7,4,'Economy'),(7,7,5,'Economy'),(7,7,6,'Economy'),(7,8,1,'Economy'),(7,8,2,'Economy'),(7,8,3,'Economy'),(7,8,4,'Economy'),(7,8,5,'Economy'),(7,8,6,'Economy'),(7,9,1,'Economy'),(7,9,2,'Economy'),(7,9,3,'Economy'),(7,9,4,'Economy'),(7,9,5,'Economy'),(7,9,6,'Economy'),(7,10,1,'Economy'),(7,10,2,'Economy'),(7,10,3,'Economy'),(7,10,4,'Economy'),(7,10,5,'Economy'),(7,10,6,'Economy'),(7,11,1,'Economy'),(7,11,2,'Economy'),(7,11,3,'Economy'),(7,11,4,'Economy'),(7,11,5,'Economy'),(7,11,6,'Economy'),(7,12,1,'Economy'),(7,12,2,'Economy'),(7,12,3,'Economy'),(7,12,4,'Economy'),(7,12,5,'Economy'),(7,12,6,'Economy'),(7,13,1,'Economy'),(7,13,2,'Economy'),(7,13,3,'Economy'),(7,13,4,'Economy'),(7,13,5,'Economy'),(7,13,6,'Economy'),(7,14,1,'Economy'),(7,14,2,'Economy'),(7,14,3,'Economy'),(7,14,4,'Economy'),(7,14,5,'Economy'),(7,14,6,'Economy'),(7,15,1,'Economy'),(7,15,2,'Economy'),(7,15,3,'Economy'),(7,15,4,'Economy'),(7,15,5,'Economy'),(7,15,6,'Economy'),(10034,1,1,'Business'),(10034,1,2,'Business'),(10034,1,3,'Business'),(10034,1,4,'Business'),(10034,2,1,'Business'),(10034,2,2,'Business'),(10034,2,3,'Business'),(10034,2,4,'Business'),(10034,3,1,'Business'),(10034,3,2,'Business'),(10034,3,3,'Business'),(10034,3,4,'Business'),(10034,10,1,'Economy'),(10034,10,2,'Economy'),(10034,10,3,'Economy'),(10034,10,4,'Economy'),(10034,11,1,'Economy'),(10034,11,2,'Economy'),(10034,11,3,'Economy'),(10034,11,4,'Economy'),(10034,12,1,'Economy'),(10034,12,2,'Economy'),(10034,12,3,'Economy'),(10034,12,4,'Economy'),(10034,13,1,'Economy'),(10034,13,2,'Economy'),(10034,13,3,'Economy'),(10034,13,4,'Economy'),(10034,14,1,'Economy'),(10034,14,2,'Economy'),(10034,14,3,'Economy'),(10034,14,4,'Economy'),(10034,15,1,'Economy'),(10034,15,2,'Economy'),(10034,15,3,'Economy'),(10034,15,4,'Economy'),(10034,16,1,'Economy'),(10034,16,2,'Economy'),(10034,16,3,'Economy'),(10034,16,4,'Economy');
/*!40000 ALTER TABLE `Seats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `UserPhones`
--

DROP TABLE IF EXISTS `UserPhones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `UserPhones` (
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone_number` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`email`,`phone_number`),
  CONSTRAINT `userphones_ibfk_1` FOREIGN KEY (`email`) REFERENCES `Users` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UserPhones`
--

LOCK TABLES `UserPhones` WRITE;
/*!40000 ALTER TABLE `UserPhones` DISABLE KEYS */;
INSERT INTO `UserPhones` (`email`, `phone_number`) VALUES ('gabi@gmail.com','0547393840'),('guest1@temp.com','052-1112223'),('guest2@temp.com','052-4445556'),('lihibarmeir@mail.tau.ac.il','050-1234567'),('noyastorzi@mail.tau.ac.il','0525339149'),('noyastorzi@mail.tau.ac.il','0526572424'),('ortalleviron@mail.tau.ac.il','05077788855'),('reg1@gmail.com','050-1234567'),('reg2@yahoo.com','050-9876543');
/*!40000 ALTER TABLE `UserPhones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` (`email`, `first_name`, `last_name`) VALUES ('gabi@gmail.com','Gabi','Berin'),('guest1@temp.com','Guest','One'),('guest2@temp.com','Guest','Two'),('lihibarmeir@mail.tau.ac.il','lihi','bar meir'),('noyastorzi@mail.tau.ac.il','noya','storzi'),('ortalleviron@mail.tau.ac.il','ortal','levi ron'),('reg1@gmail.com','John','Doe'),('reg2@yahoo.com','Jane','Smith');
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'flytau'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-22 17:46:41
