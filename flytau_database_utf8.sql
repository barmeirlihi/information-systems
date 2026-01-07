-- MySQL dump 10.13  Distrib 8.0.44, for macos15 (arm64)
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
INSERT INTO `Airports` VALUES ('CDG','France','Paris'),('JFK','USA','New York'),('LHR','UK','London'),('TLV','Israel','Tel Aviv');
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
INSERT INTO `Attendants` VALUES ('100000001','נועה','קירל','054-1000001','Tel Aviv','HaYarkon','1','2022-01-01',1),('100000002','אנה','זק','054-1000002','Ashdod','HaYam','2','2022-01-02',1),('100000003','יונתן','מרגי','054-1000003','Yehud','HaAtzmaut','3','2022-01-03',0),('100000004','סטטיק','רוסו','054-1000004','Haifa','Moriah','4','2022-01-04',1),('100000005','בן','תבורי','054-1000005','Tel Aviv','Dizengoff','5','2022-01-05',0),('100000006','אגס','קימל','054-1000006','Tel Aviv','Rothschild','6','2022-01-06',0),('100000007','עדן','בן זקן','054-1000007','Kiryat Shmona','HaHagana','7','2022-01-07',1),('100000008','נטע','ברזילי','054-1000008','Hod HaSharon','HaBanim','8','2022-01-08',1),('100000009','רן','דנקר','054-1000009','Tel Aviv','Shenkin','9','2022-01-09',1),('100000010','עברי','לידר','054-1000010','Tel Aviv','Melchet','10','2022-01-10',1),('100000011','הראל','סקעת','054-1000011','Kfar Saba','HaKikar','11','2022-01-11',0),('100000012','שירי','מימון','054-1000012','Haifa','HaNassi','12','2022-01-12',1),('100000013','נינט','טייב','054-1000013','Kiryat Gat','Lachish','13','2022-01-13',1),('100000014','אביב','גפן','054-1000014','Tzahala','HaMishtala','14','2022-01-14',0),('100000015','אייל','גולן','054-1000015','Rehovot','Herzl','15','2022-01-15',1),('100000016','משה','פרץ','054-1000016','Tiberias','HaGalil','16','2022-01-16',0),('100000017','עומר','אדם','054-1000017','Mishmar HaShiva','HaZayit','17','2022-01-17',1),('100000018','דודו','אהרון','054-1000018','Ekron','HaRimon','18','2022-01-18',0),('100000019','קובי','פרץ','054-1000019','Tel Aviv','HaYarkon','19','2022-01-19',1),('100000020','שרית','חדד','054-1000020','Hadera','HaNassi','20','2022-01-20',1);
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
INSERT INTO `FlightRoutes` VALUES ('CDG','TLV',270),('JFK','TLV',660),('TLV','JFK',720),('TLV','LHR',300);
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
INSERT INTO `Flights` VALUES (1001,'08:00:00','2026-06-01','Active',1,'TLV','JFK',600.00,1200.00),(1002,'14:00:00','2026-06-02','Active',2,'TLV','LHR',300.00,NULL),(1003,'10:00:00','2026-07-10','Active',3,'CDG','TLV',550.00,1100.00),(1004,'23:00:00','2026-08-15','Active',1,'JFK','TLV',700.00,1500.00);
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
INSERT INTO `FlightTickets` VALUES (501,1001,1,1,1),(502,1001,1,1,2),(503,1002,2,1,1),(504,1002,2,1,2);
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
INSERT INTO `Guests` VALUES ('benporat3@mail.tau.ac.il'),('gabi@gmail.com'),('guest1@temp.com'),('guest2@temp.com'),('noyastorzi@mail.tau.ac.il');
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
INSERT INTO `Managers` VALUES ('300000001','מנהל','ראשי','050-1111111','Tel Aviv','Rothschild','10','2015-01-01','admin123'),('300000002','מנהל','משני','050-2222222','Haifa','Herzl','5','2018-06-01','admin456');
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
INSERT INTO `Orders` VALUES (501,'reg1@gmail.com','Confirmed','2026-01-10',1200.00),(502,'guest1@temp.com','Confirmed','2026-01-12',1200.00),(503,'reg2@yahoo.com','Confirmed','2026-02-05',300.00),(504,'guest2@temp.com','Confirmed','2026-03-20',300.00);
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
INSERT INTO `Pilots` VALUES ('200000001','ישראל','ישראלי','052-1000001','Ramat Gan','HaRoeh','1','2019-01-01',1),('200000002','דוד','כהן','052-1000002','Givatayim','Weizmann','2','2019-02-01',1),('200000003','משה','לוי','052-1000003','Holon','Sokolov','3','2020-03-01',0),('200000004','יעקב','אברהם','052-1000004','Bat Yam','Jerusalem','4','2020-04-01',1),('200000005','יצחק','רבין','052-1000005','Rishon LeZion','Jabotinsky','5','2021-05-01',0),('200000006','חיים','נחמן','052-1000006','Petah Tikva','HaHistadrut','6','2021-06-01',1),('200000007','שאול','מופז','052-1000007','Netanya','Herzl','7','2022-07-01',0),('200000008','אהוד','ברק','052-1000008','Herzliya','HaBanim','8','2022-08-01',1),('200000009','אריאל','שרון','052-1000009','Kfar Saba','Weizmann','9','2023-09-01',0),('200000010','מנחם','בגין','052-1000010','Ra\'anana','Ahuza','10','2023-10-01',1);
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
INSERT INTO `Planes` VALUES (1,'Boeing','Large','2020-01-01'),(2,'Boeing','Small','2021-05-15'),(3,'Airbus','Large','2019-11-20'),(4,'Airbus','Small','2022-03-10'),(5,'Boeing','Large','2018-08-08'),(6,'Dassault','Small','2023-01-01');
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
INSERT INTO `RegisteredUsers` VALUES ('lihibarmeir@mail.tau.ac.il','lihi1234','3245876938','2000-11-21','2026-01-04'),('reg1@gmail.com','pass123','P100200300','1990-05-15','2024-01-01'),('reg2@yahoo.com','pass456','P400500600','1995-08-20','2024-02-10');
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
INSERT INTO `Seats` VALUES (1,1,1,'Business'),(1,1,2,'Business'),(1,1,3,'Business'),(1,1,4,'Business'),(1,2,1,'Business'),(1,2,2,'Business'),(1,2,3,'Business'),(1,2,4,'Business'),(1,3,1,'Business'),(1,3,2,'Business'),(1,3,3,'Business'),(1,3,4,'Business'),(1,4,1,'Business'),(1,4,2,'Business'),(1,4,3,'Business'),(1,4,4,'Business'),(1,10,1,'Economy'),(1,10,2,'Economy'),(1,10,3,'Economy'),(1,10,4,'Economy'),(1,10,5,'Economy'),(1,10,6,'Economy'),(1,11,1,'Economy'),(1,11,2,'Economy'),(1,11,3,'Economy'),(1,11,4,'Economy'),(1,11,5,'Economy'),(1,11,6,'Economy'),(1,12,1,'Economy'),(1,12,2,'Economy'),(1,12,3,'Economy'),(1,12,4,'Economy'),(1,12,5,'Economy'),(1,12,6,'Economy'),(1,13,1,'Economy'),(1,13,2,'Economy'),(1,13,3,'Economy'),(1,13,4,'Economy'),(1,13,5,'Economy'),(1,13,6,'Economy'),(1,14,1,'Economy'),(1,14,2,'Economy'),(1,14,3,'Economy'),(1,14,4,'Economy'),(1,14,5,'Economy'),(1,14,6,'Economy'),(1,15,1,'Economy'),(1,15,2,'Economy'),(1,15,3,'Economy'),(1,15,4,'Economy'),(1,15,5,'Economy'),(1,15,6,'Economy'),(1,16,1,'Economy'),(1,16,2,'Economy'),(1,16,3,'Economy'),(1,16,4,'Economy'),(1,16,5,'Economy'),(1,16,6,'Economy'),(1,17,1,'Economy'),(1,17,2,'Economy'),(1,17,3,'Economy'),(1,17,4,'Economy'),(1,17,5,'Economy'),(1,17,6,'Economy'),(1,18,1,'Economy'),(1,18,2,'Economy'),(1,18,3,'Economy'),(1,18,4,'Economy'),(1,18,5,'Economy'),(1,18,6,'Economy'),(1,19,1,'Economy'),(1,19,2,'Economy'),(1,19,3,'Economy'),(1,19,4,'Economy'),(1,19,5,'Economy'),(1,19,6,'Economy'),(1,20,1,'Economy'),(1,20,2,'Economy'),(1,20,3,'Economy'),(1,20,4,'Economy'),(1,20,5,'Economy'),(1,20,6,'Economy'),(2,1,1,'Economy'),(2,1,2,'Economy'),(2,1,3,'Economy'),(2,1,4,'Economy'),(2,1,5,'Economy'),(2,1,6,'Economy'),(2,2,1,'Economy'),(2,2,2,'Economy'),(2,2,3,'Economy'),(2,2,4,'Economy'),(2,2,5,'Economy'),(2,2,6,'Economy'),(2,3,1,'Economy'),(2,3,2,'Economy'),(2,3,3,'Economy'),(2,3,4,'Economy'),(2,3,5,'Economy'),(2,3,6,'Economy'),(2,4,1,'Economy'),(2,4,2,'Economy'),(2,4,3,'Economy'),(2,4,4,'Economy'),(2,4,5,'Economy'),(2,4,6,'Economy'),(2,5,1,'Economy'),(2,5,2,'Economy'),(2,5,3,'Economy'),(2,5,4,'Economy'),(2,5,5,'Economy'),(2,5,6,'Economy'),(2,6,1,'Economy'),(2,6,2,'Economy'),(2,6,3,'Economy'),(2,6,4,'Economy'),(2,6,5,'Economy'),(2,6,6,'Economy'),(2,7,1,'Economy'),(2,7,2,'Economy'),(2,7,3,'Economy'),(2,7,4,'Economy'),(2,7,5,'Economy'),(2,7,6,'Economy'),(2,8,1,'Economy'),(2,8,2,'Economy'),(2,8,3,'Economy'),(2,8,4,'Economy'),(2,8,5,'Economy'),(2,8,6,'Economy'),(2,9,1,'Economy'),(2,9,2,'Economy'),(2,9,3,'Economy'),(2,9,4,'Economy'),(2,9,5,'Economy'),(2,9,6,'Economy'),(2,10,1,'Economy'),(2,10,2,'Economy'),(2,10,3,'Economy'),(2,10,4,'Economy'),(2,10,5,'Economy'),(2,10,6,'Economy'),(2,11,1,'Economy'),(2,11,2,'Economy'),(2,11,3,'Economy'),(2,11,4,'Economy'),(2,11,5,'Economy'),(2,11,6,'Economy'),(2,12,1,'Economy'),(2,12,2,'Economy'),(2,12,3,'Economy'),(2,12,4,'Economy'),(2,12,5,'Economy'),(2,12,6,'Economy'),(2,13,1,'Economy'),(2,13,2,'Economy'),(2,13,3,'Economy'),(2,13,4,'Economy'),(2,13,5,'Economy'),(2,13,6,'Economy'),(2,14,1,'Economy'),(2,14,2,'Economy'),(2,14,3,'Economy'),(2,14,4,'Economy'),(2,14,5,'Economy'),(2,14,6,'Economy'),(2,15,1,'Economy'),(2,15,2,'Economy'),(2,15,3,'Economy'),(2,15,4,'Economy'),(2,15,5,'Economy'),(2,15,6,'Economy'),(3,1,1,'Business'),(3,1,2,'Business'),(3,1,3,'Business'),(3,1,4,'Business'),(3,2,1,'Business'),(3,2,2,'Business'),(3,2,3,'Business'),(3,2,4,'Business'),(3,10,1,'Economy'),(3,10,2,'Economy'),(3,10,3,'Economy'),(3,10,4,'Economy'),(3,10,5,'Economy'),(3,10,6,'Economy'),(3,11,1,'Economy'),(3,11,2,'Economy'),(3,11,3,'Economy'),(3,11,4,'Economy'),(3,11,5,'Economy'),(3,11,6,'Economy'),(3,12,1,'Economy'),(3,12,2,'Economy'),(3,12,3,'Economy'),(3,12,4,'Economy'),(3,12,5,'Economy'),(3,12,6,'Economy'),(3,13,1,'Economy'),(3,13,2,'Economy'),(3,13,3,'Economy'),(3,13,4,'Economy'),(3,13,5,'Economy'),(3,13,6,'Economy'),(3,14,1,'Economy'),(3,14,2,'Economy'),(3,14,3,'Economy'),(3,14,4,'Economy'),(3,14,5,'Economy'),(3,14,6,'Economy'),(3,15,1,'Economy'),(3,15,2,'Economy'),(3,15,3,'Economy'),(3,15,4,'Economy'),(3,15,5,'Economy'),(3,15,6,'Economy'),(4,1,1,'Economy'),(4,1,2,'Economy'),(4,1,3,'Economy'),(4,1,4,'Economy'),(4,1,5,'Economy'),(4,1,6,'Economy'),(4,2,1,'Economy'),(4,2,2,'Economy'),(4,2,3,'Economy'),(4,2,4,'Economy'),(4,2,5,'Economy'),(4,2,6,'Economy'),(4,3,1,'Economy'),(4,3,2,'Economy'),(4,3,3,'Economy'),(4,3,4,'Economy'),(4,3,5,'Economy'),(4,3,6,'Economy'),(4,4,1,'Economy'),(4,4,2,'Economy'),(4,4,3,'Economy'),(4,4,4,'Economy'),(4,4,5,'Economy'),(4,4,6,'Economy'),(4,5,1,'Economy'),(4,5,2,'Economy'),(4,5,3,'Economy'),(4,5,4,'Economy'),(4,5,5,'Economy'),(4,5,6,'Economy'),(4,6,1,'Economy'),(4,6,2,'Economy'),(4,6,3,'Economy'),(4,6,4,'Economy'),(4,6,5,'Economy'),(4,6,6,'Economy'),(4,7,1,'Economy'),(4,7,2,'Economy'),(4,7,3,'Economy'),(4,7,4,'Economy'),(4,7,5,'Economy'),(4,7,6,'Economy'),(4,8,1,'Economy'),(4,8,2,'Economy'),(4,8,3,'Economy'),(4,8,4,'Economy'),(4,8,5,'Economy'),(4,8,6,'Economy'),(4,9,1,'Economy'),(4,9,2,'Economy'),(4,9,3,'Economy'),(4,9,4,'Economy'),(4,9,5,'Economy'),(4,9,6,'Economy'),(4,10,1,'Economy'),(4,10,2,'Economy'),(4,10,3,'Economy'),(4,10,4,'Economy'),(4,10,5,'Economy'),(4,10,6,'Economy'),(5,1,1,'Business'),(5,1,2,'Business'),(5,1,3,'Business'),(5,1,4,'Business'),(5,10,1,'Economy'),(5,10,2,'Economy'),(5,10,3,'Economy'),(5,10,4,'Economy'),(5,10,5,'Economy'),(5,10,6,'Economy'),(5,11,1,'Economy'),(5,11,2,'Economy'),(5,11,3,'Economy'),(5,11,4,'Economy'),(5,11,5,'Economy'),(5,11,6,'Economy'),(5,12,1,'Economy'),(5,12,2,'Economy'),(5,12,3,'Economy'),(5,12,4,'Economy'),(5,12,5,'Economy'),(5,12,6,'Economy'),(6,1,1,'Economy'),(6,1,2,'Economy'),(6,1,3,'Economy'),(6,1,4,'Economy'),(6,2,1,'Economy'),(6,2,2,'Economy'),(6,2,3,'Economy'),(6,2,4,'Economy'),(6,3,1,'Economy'),(6,3,2,'Economy'),(6,3,3,'Economy'),(6,3,4,'Economy'),(6,4,1,'Economy'),(6,4,2,'Economy'),(6,4,3,'Economy'),(6,4,4,'Economy'),(6,5,1,'Economy'),(6,5,2,'Economy'),(6,5,3,'Economy'),(6,5,4,'Economy'),(6,6,1,'Economy'),(6,6,2,'Economy'),(6,6,3,'Economy'),(6,6,4,'Economy'),(6,7,1,'Economy'),(6,7,2,'Economy'),(6,7,3,'Economy'),(6,7,4,'Economy'),(6,8,1,'Economy'),(6,8,2,'Economy'),(6,8,3,'Economy'),(6,8,4,'Economy'),(6,9,1,'Economy'),(6,9,2,'Economy'),(6,9,3,'Economy'),(6,9,4,'Economy'),(6,10,1,'Economy'),(6,10,2,'Economy'),(6,10,3,'Economy'),(6,10,4,'Economy');
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
INSERT INTO `UserPhones` VALUES ('gabi@gmail.com','0547393840'),('guest1@temp.com','052-1112223'),('guest2@temp.com','052-4445556'),('lihibarmeir@mail.tau.ac.il','050-1234567'),('reg1@gmail.com','050-1234567'),('reg2@yahoo.com','050-9876543');
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
INSERT INTO `Users` VALUES ('benporat3@mail.tau.ac.il','liron','benpo'),('gabi@gmail.com','Gabi','Hameleh'),('guest1@temp.com','Guest','One'),('guest2@temp.com','Guest','Two'),('lihibarmeir@mail.tau.ac.il','lihi','bar meir'),('noyastorzi@mail.tau.ac.il','noya','storzi'),('ortalleviron@mail.tau.ac.il','ortal','levi ron'),('reg1@gmail.com','John','Doe'),('reg2@yahoo.com','Jane','Smith');
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-07  8:11:40
