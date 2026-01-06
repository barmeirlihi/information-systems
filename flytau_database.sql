-- FlyTau Database Export
-- Generated automatically

SET FOREIGN_KEY_CHECKS=0;

-- Table: Airports
DROP TABLE IF EXISTS `Airports`;

CREATE TABLE `Airports` (
  `airport_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `country` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `city` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`airport_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table `Airports`
INSERT INTO `Airports` (`airport_name`, `country`, `city`) VALUES ('CDG', 'France', 'Paris');
INSERT INTO `Airports` (`airport_name`, `country`, `city`) VALUES ('JFK', 'USA', 'New York');
INSERT INTO `Airports` (`airport_name`, `country`, `city`) VALUES ('LHR', 'UK', 'London');
INSERT INTO `Airports` (`airport_name`, `country`, `city`) VALUES ('TLV', 'Israel', 'Tel Aviv');

-- Table: Attendants
DROP TABLE IF EXISTS `Attendants`;

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

-- Data for table `Attendants`
INSERT INTO `Attendants` (`attendant_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('100000001', 'נועה', 'קירל', '054-1000001', 'Tel Aviv', 'HaYarkon', '1', 2022-01-01, 1);
INSERT INTO `Attendants` (`attendant_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('100000002', 'אנה', 'זק', '054-1000002', 'Ashdod', 'HaYam', '2', 2022-01-02, 1);
INSERT INTO `Attendants` (`attendant_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('100000003', 'יונתן', 'מרגי', '054-1000003', 'Yehud', 'HaAtzmaut', '3', 2022-01-03, 0);
INSERT INTO `Attendants` (`attendant_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('100000004', 'סטטיק', 'רוסו', '054-1000004', 'Haifa', 'Moriah', '4', 2022-01-04, 1);
INSERT INTO `Attendants` (`attendant_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('100000005', 'בן', 'תבורי', '054-1000005', 'Tel Aviv', 'Dizengoff', '5', 2022-01-05, 0);
INSERT INTO `Attendants` (`attendant_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('100000006', 'אגס', 'קימל', '054-1000006', 'Tel Aviv', 'Rothschild', '6', 2022-01-06, 0);
INSERT INTO `Attendants` (`attendant_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('100000007', 'עדן', 'בן זקן', '054-1000007', 'Kiryat Shmona', 'HaHagana', '7', 2022-01-07, 1);
INSERT INTO `Attendants` (`attendant_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('100000008', 'נטע', 'ברזילי', '054-1000008', 'Hod HaSharon', 'HaBanim', '8', 2022-01-08, 1);
INSERT INTO `Attendants` (`attendant_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('100000009', 'רן', 'דנקר', '054-1000009', 'Tel Aviv', 'Shenkin', '9', 2022-01-09, 1);
INSERT INTO `Attendants` (`attendant_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('100000010', 'עברי', 'לידר', '054-1000010', 'Tel Aviv', 'Melchet', '10', 2022-01-10, 1);
INSERT INTO `Attendants` (`attendant_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('100000011', 'הראל', 'סקעת', '054-1000011', 'Kfar Saba', 'HaKikar', '11', 2022-01-11, 0);
INSERT INTO `Attendants` (`attendant_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('100000012', 'שירי', 'מימון', '054-1000012', 'Haifa', 'HaNassi', '12', 2022-01-12, 1);
INSERT INTO `Attendants` (`attendant_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('100000013', 'נינט', 'טייב', '054-1000013', 'Kiryat Gat', 'Lachish', '13', 2022-01-13, 1);
INSERT INTO `Attendants` (`attendant_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('100000014', 'אביב', 'גפן', '054-1000014', 'Tzahala', 'HaMishtala', '14', 2022-01-14, 0);
INSERT INTO `Attendants` (`attendant_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('100000015', 'אייל', 'גולן', '054-1000015', 'Rehovot', 'Herzl', '15', 2022-01-15, 1);
INSERT INTO `Attendants` (`attendant_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('100000016', 'משה', 'פרץ', '054-1000016', 'Tiberias', 'HaGalil', '16', 2022-01-16, 0);
INSERT INTO `Attendants` (`attendant_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('100000017', 'עומר', 'אדם', '054-1000017', 'Mishmar HaShiva', 'HaZayit', '17', 2022-01-17, 1);
INSERT INTO `Attendants` (`attendant_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('100000018', 'דודו', 'אהרון', '054-1000018', 'Ekron', 'HaRimon', '18', 2022-01-18, 0);
INSERT INTO `Attendants` (`attendant_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('100000019', 'קובי', 'פרץ', '054-1000019', 'Tel Aviv', 'HaYarkon', '19', 2022-01-19, 1);
INSERT INTO `Attendants` (`attendant_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('100000020', 'שרית', 'חדד', '054-1000020', 'Hadera', 'HaNassi', '20', 2022-01-20, 1);

-- Table: Attendants_In_Flights
DROP TABLE IF EXISTS `Attendants_In_Flights`;

CREATE TABLE `Attendants_In_Flights` (
  `attendant_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `flight_id` int NOT NULL,
  PRIMARY KEY (`attendant_id`,`flight_id`),
  KEY `flight_id` (`flight_id`),
  CONSTRAINT `attendants_in_flights_ibfk_1` FOREIGN KEY (`attendant_id`) REFERENCES `Attendants` (`attendant_id`),
  CONSTRAINT `attendants_in_flights_ibfk_2` FOREIGN KEY (`flight_id`) REFERENCES `Flights` (`flight_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: FlightRoutes
DROP TABLE IF EXISTS `FlightRoutes`;

CREATE TABLE `FlightRoutes` (
  `origin_airport_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `destination_airport_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `flight_duration` int NOT NULL,
  PRIMARY KEY (`origin_airport_name`,`destination_airport_name`),
  KEY `destination_airport_name` (`destination_airport_name`),
  CONSTRAINT `flightroutes_ibfk_1` FOREIGN KEY (`origin_airport_name`) REFERENCES `Airports` (`airport_name`),
  CONSTRAINT `flightroutes_ibfk_2` FOREIGN KEY (`destination_airport_name`) REFERENCES `Airports` (`airport_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table `FlightRoutes`
INSERT INTO `FlightRoutes` (`origin_airport_name`, `destination_airport_name`, `flight_duration`) VALUES ('CDG', 'TLV', 270);
INSERT INTO `FlightRoutes` (`origin_airport_name`, `destination_airport_name`, `flight_duration`) VALUES ('JFK', 'TLV', 660);
INSERT INTO `FlightRoutes` (`origin_airport_name`, `destination_airport_name`, `flight_duration`) VALUES ('TLV', 'JFK', 720);
INSERT INTO `FlightRoutes` (`origin_airport_name`, `destination_airport_name`, `flight_duration`) VALUES ('TLV', 'LHR', 300);

-- Table: Flights
DROP TABLE IF EXISTS `Flights`;

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

-- Data for table `Flights`
INSERT INTO `Flights` (`flight_id`, `departure_time`, `departure_date`, `status`, `plane_id`, `origin_airport_name`, `destination_airport_name`, `price_economy`, `price_business`) VALUES (1001, 8:00:00, 2026-06-01, 'Active', 1, 'TLV', 'JFK', 600.00, 1200.00);
INSERT INTO `Flights` (`flight_id`, `departure_time`, `departure_date`, `status`, `plane_id`, `origin_airport_name`, `destination_airport_name`, `price_economy`, `price_business`) VALUES (1002, 14:00:00, 2026-06-02, 'Active', 2, 'TLV', 'LHR', 300.00, NULL);
INSERT INTO `Flights` (`flight_id`, `departure_time`, `departure_date`, `status`, `plane_id`, `origin_airport_name`, `destination_airport_name`, `price_economy`, `price_business`) VALUES (1003, 10:00:00, 2026-07-10, 'Active', 3, 'CDG', 'TLV', 550.00, 1100.00);
INSERT INTO `Flights` (`flight_id`, `departure_time`, `departure_date`, `status`, `plane_id`, `origin_airport_name`, `destination_airport_name`, `price_economy`, `price_business`) VALUES (1004, 23:00:00, 2026-08-15, 'Active', 1, 'JFK', 'TLV', 700.00, 1500.00);

-- Table: FlightTickets
DROP TABLE IF EXISTS `FlightTickets`;

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

-- Data for table `FlightTickets`
INSERT INTO `FlightTickets` (`order_id`, `flight_id`, `plane_id`, `seat_row`, `seat_column`) VALUES (501, 1001, 1, 1, 1);
INSERT INTO `FlightTickets` (`order_id`, `flight_id`, `plane_id`, `seat_row`, `seat_column`) VALUES (502, 1001, 1, 1, 2);
INSERT INTO `FlightTickets` (`order_id`, `flight_id`, `plane_id`, `seat_row`, `seat_column`) VALUES (503, 1002, 2, 1, 1);
INSERT INTO `FlightTickets` (`order_id`, `flight_id`, `plane_id`, `seat_row`, `seat_column`) VALUES (504, 1002, 2, 1, 2);

-- Table: Guests
DROP TABLE IF EXISTS `Guests`;

CREATE TABLE `Guests` (
  `UserEmail` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`UserEmail`),
  CONSTRAINT `guests_ibfk_1` FOREIGN KEY (`UserEmail`) REFERENCES `Users` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table `Guests`
INSERT INTO `Guests` (`UserEmail`) VALUES ('benporat3@mail.tau.ac.il');
INSERT INTO `Guests` (`UserEmail`) VALUES ('gabi@gmail.com');
INSERT INTO `Guests` (`UserEmail`) VALUES ('guest1@temp.com');
INSERT INTO `Guests` (`UserEmail`) VALUES ('guest2@temp.com');
INSERT INTO `Guests` (`UserEmail`) VALUES ('noyastorzi@mail.tau.ac.il');

-- Table: Managers
DROP TABLE IF EXISTS `Managers`;

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

-- Data for table `Managers`
INSERT INTO `Managers` (`manager_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `password`) VALUES ('300000001', 'מנהל', 'ראשי', '050-1111111', 'Tel Aviv', 'Rothschild', '10', 2015-01-01, 'admin123');
INSERT INTO `Managers` (`manager_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `password`) VALUES ('300000002', 'מנהל', 'משני', '050-2222222', 'Haifa', 'Herzl', '5', 2018-06-01, 'admin456');

-- Table: Orders
DROP TABLE IF EXISTS `Orders`;

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

-- Data for table `Orders`
INSERT INTO `Orders` (`order_id`, `email`, `order_status`, `order_date`, `total_payment`) VALUES (501, 'reg1@gmail.com', 'Confirmed', 2026-01-10, 1200.00);
INSERT INTO `Orders` (`order_id`, `email`, `order_status`, `order_date`, `total_payment`) VALUES (502, 'guest1@temp.com', 'Confirmed', 2026-01-12, 1200.00);
INSERT INTO `Orders` (`order_id`, `email`, `order_status`, `order_date`, `total_payment`) VALUES (503, 'reg2@yahoo.com', 'Confirmed', 2026-02-05, 300.00);
INSERT INTO `Orders` (`order_id`, `email`, `order_status`, `order_date`, `total_payment`) VALUES (504, 'guest2@temp.com', 'Confirmed', 2026-03-20, 300.00);

-- Table: Pilots
DROP TABLE IF EXISTS `Pilots`;

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

-- Data for table `Pilots`
INSERT INTO `Pilots` (`pilot_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('200000001', 'ישראל', 'ישראלי', '052-1000001', 'Ramat Gan', 'HaRoeh', '1', 2019-01-01, 1);
INSERT INTO `Pilots` (`pilot_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('200000002', 'דוד', 'כהן', '052-1000002', 'Givatayim', 'Weizmann', '2', 2019-02-01, 1);
INSERT INTO `Pilots` (`pilot_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('200000003', 'משה', 'לוי', '052-1000003', 'Holon', 'Sokolov', '3', 2020-03-01, 0);
INSERT INTO `Pilots` (`pilot_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('200000004', 'יעקב', 'אברהם', '052-1000004', 'Bat Yam', 'Jerusalem', '4', 2020-04-01, 1);
INSERT INTO `Pilots` (`pilot_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('200000005', 'יצחק', 'רבין', '052-1000005', 'Rishon LeZion', 'Jabotinsky', '5', 2021-05-01, 0);
INSERT INTO `Pilots` (`pilot_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('200000006', 'חיים', 'נחמן', '052-1000006', 'Petah Tikva', 'HaHistadrut', '6', 2021-06-01, 1);
INSERT INTO `Pilots` (`pilot_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('200000007', 'שאול', 'מופז', '052-1000007', 'Netanya', 'Herzl', '7', 2022-07-01, 0);
INSERT INTO `Pilots` (`pilot_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('200000008', 'אהוד', 'ברק', '052-1000008', 'Herzliya', 'HaBanim', '8', 2022-08-01, 1);
INSERT INTO `Pilots` (`pilot_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('200000009', 'אריאל', 'שרון', '052-1000009', 'Kfar Saba', 'Weizmann', '9', 2023-09-01, 0);
INSERT INTO `Pilots` (`pilot_id`, `first_name_he`, `last_name_he`, `phone_number`, `city`, `street`, `house_number`, `start_work_date`, `long_flight_certified`) VALUES ('200000010', 'מנחם', 'בגין', '052-1000010', 'Ra''anana', 'Ahuza', '10', 2023-10-01, 1);

-- Table: Pilots_In_Flights
DROP TABLE IF EXISTS `Pilots_In_Flights`;

CREATE TABLE `Pilots_In_Flights` (
  `pilot_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `flight_id` int NOT NULL,
  PRIMARY KEY (`pilot_id`,`flight_id`),
  KEY `flight_id` (`flight_id`),
  CONSTRAINT `pilots_in_flights_ibfk_1` FOREIGN KEY (`pilot_id`) REFERENCES `Pilots` (`pilot_id`),
  CONSTRAINT `pilots_in_flights_ibfk_2` FOREIGN KEY (`flight_id`) REFERENCES `Flights` (`flight_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: Planes
DROP TABLE IF EXISTS `Planes`;

CREATE TABLE `Planes` (
  `plane_id` int NOT NULL,
  `manufacturer` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `size` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `purchase_date` date NOT NULL,
  PRIMARY KEY (`plane_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table `Planes`
INSERT INTO `Planes` (`plane_id`, `manufacturer`, `size`, `purchase_date`) VALUES (1, 'Boeing', 'Large', 2020-01-01);
INSERT INTO `Planes` (`plane_id`, `manufacturer`, `size`, `purchase_date`) VALUES (2, 'Boeing', 'Small', 2021-05-15);
INSERT INTO `Planes` (`plane_id`, `manufacturer`, `size`, `purchase_date`) VALUES (3, 'Airbus', 'Large', 2019-11-20);
INSERT INTO `Planes` (`plane_id`, `manufacturer`, `size`, `purchase_date`) VALUES (4, 'Airbus', 'Small', 2022-03-10);
INSERT INTO `Planes` (`plane_id`, `manufacturer`, `size`, `purchase_date`) VALUES (5, 'Boeing', 'Large', 2018-08-08);
INSERT INTO `Planes` (`plane_id`, `manufacturer`, `size`, `purchase_date`) VALUES (6, 'Dassault', 'Small', 2023-01-01);

-- Table: RegisteredUsers
DROP TABLE IF EXISTS `RegisteredUsers`;

CREATE TABLE `RegisteredUsers` (
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `passport_number` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `birth_date` date NOT NULL,
  `registration_date` date NOT NULL,
  PRIMARY KEY (`email`),
  CONSTRAINT `registeredusers_ibfk_1` FOREIGN KEY (`email`) REFERENCES `Users` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table `RegisteredUsers`
INSERT INTO `RegisteredUsers` (`email`, `password`, `passport_number`, `birth_date`, `registration_date`) VALUES ('lihibarmeir@mail.tau.ac.il', 'lihi1234', '3245876938', 2000-11-21, 2026-01-04);
INSERT INTO `RegisteredUsers` (`email`, `password`, `passport_number`, `birth_date`, `registration_date`) VALUES ('reg1@gmail.com', 'pass123', 'P100200300', 1990-05-15, 2024-01-01);
INSERT INTO `RegisteredUsers` (`email`, `password`, `passport_number`, `birth_date`, `registration_date`) VALUES ('reg2@yahoo.com', 'pass456', 'P400500600', 1995-08-20, 2024-02-10);

-- Table: Seats
DROP TABLE IF EXISTS `Seats`;

CREATE TABLE `Seats` (
  `plane_id` int NOT NULL,
  `seat_row` int NOT NULL,
  `seat_column` int NOT NULL,
  `seat_class` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`plane_id`,`seat_row`,`seat_column`),
  CONSTRAINT `seats_ibfk_1` FOREIGN KEY (`plane_id`) REFERENCES `Planes` (`plane_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table `Seats`
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 1, 1, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 1, 2, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 1, 3, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 1, 4, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 2, 1, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 2, 2, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 2, 3, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 2, 4, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 3, 1, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 3, 2, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 3, 3, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 3, 4, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 4, 1, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 4, 2, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 4, 3, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 4, 4, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 10, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 10, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 10, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 10, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 10, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 10, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 11, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 11, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 11, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 11, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 11, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 11, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 12, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 12, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 12, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 12, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 12, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 12, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 13, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 13, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 13, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 13, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 13, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 13, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 14, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 14, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 14, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 14, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 14, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 14, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 15, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 15, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 15, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 15, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 15, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 15, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 16, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 16, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 16, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 16, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 16, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 16, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 17, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 17, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 17, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 17, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 17, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 17, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 18, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 18, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 18, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 18, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 18, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 18, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 19, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 19, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 19, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 19, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 19, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 19, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 20, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 20, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 20, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 20, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 20, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (1, 20, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 1, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 1, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 1, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 1, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 1, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 1, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 2, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 2, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 2, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 2, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 2, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 2, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 3, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 3, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 3, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 3, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 3, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 3, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 4, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 4, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 4, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 4, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 4, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 4, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 5, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 5, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 5, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 5, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 5, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 5, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 6, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 6, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 6, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 6, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 6, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 6, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 7, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 7, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 7, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 7, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 7, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 7, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 8, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 8, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 8, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 8, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 8, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 8, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 9, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 9, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 9, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 9, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 9, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 9, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 10, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 10, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 10, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 10, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 10, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 10, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 11, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 11, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 11, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 11, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 11, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 11, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 12, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 12, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 12, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 12, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 12, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 12, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 13, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 13, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 13, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 13, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 13, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 13, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 14, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 14, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 14, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 14, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 14, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 14, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 15, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 15, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 15, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 15, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 15, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (2, 15, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 1, 1, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 1, 2, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 1, 3, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 1, 4, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 2, 1, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 2, 2, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 2, 3, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 2, 4, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 10, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 10, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 10, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 10, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 10, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 10, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 11, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 11, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 11, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 11, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 11, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 11, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 12, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 12, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 12, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 12, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 12, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 12, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 13, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 13, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 13, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 13, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 13, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 13, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 14, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 14, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 14, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 14, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 14, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 14, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 15, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 15, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 15, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 15, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 15, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (3, 15, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 1, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 1, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 1, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 1, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 1, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 1, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 2, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 2, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 2, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 2, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 2, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 2, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 3, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 3, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 3, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 3, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 3, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 3, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 4, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 4, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 4, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 4, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 4, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 4, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 5, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 5, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 5, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 5, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 5, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 5, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 6, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 6, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 6, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 6, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 6, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 6, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 7, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 7, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 7, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 7, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 7, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 7, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 8, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 8, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 8, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 8, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 8, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 8, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 9, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 9, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 9, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 9, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 9, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 9, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 10, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 10, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 10, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 10, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 10, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (4, 10, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (5, 1, 1, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (5, 1, 2, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (5, 1, 3, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (5, 1, 4, 'Business');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (5, 10, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (5, 10, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (5, 10, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (5, 10, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (5, 10, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (5, 10, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (5, 11, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (5, 11, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (5, 11, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (5, 11, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (5, 11, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (5, 11, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (5, 12, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (5, 12, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (5, 12, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (5, 12, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (5, 12, 5, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (5, 12, 6, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 1, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 1, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 1, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 1, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 2, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 2, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 2, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 2, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 3, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 3, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 3, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 3, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 4, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 4, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 4, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 4, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 5, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 5, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 5, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 5, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 6, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 6, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 6, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 6, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 7, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 7, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 7, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 7, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 8, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 8, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 8, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 8, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 9, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 9, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 9, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 9, 4, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 10, 1, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 10, 2, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 10, 3, 'Economy');
INSERT INTO `Seats` (`plane_id`, `seat_row`, `seat_column`, `seat_class`) VALUES (6, 10, 4, 'Economy');

-- Table: UserPhones
DROP TABLE IF EXISTS `UserPhones`;

CREATE TABLE `UserPhones` (
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone_number` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`email`,`phone_number`),
  CONSTRAINT `userphones_ibfk_1` FOREIGN KEY (`email`) REFERENCES `Users` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table `UserPhones`
INSERT INTO `UserPhones` (`email`, `phone_number`) VALUES ('gabi@gmail.com', '0547393840');
INSERT INTO `UserPhones` (`email`, `phone_number`) VALUES ('guest1@temp.com', '052-1112223');
INSERT INTO `UserPhones` (`email`, `phone_number`) VALUES ('guest2@temp.com', '052-4445556');
INSERT INTO `UserPhones` (`email`, `phone_number`) VALUES ('lihibarmeir@mail.tau.ac.il', '050-1234567');
INSERT INTO `UserPhones` (`email`, `phone_number`) VALUES ('reg1@gmail.com', '050-1234567');
INSERT INTO `UserPhones` (`email`, `phone_number`) VALUES ('reg2@yahoo.com', '050-9876543');

-- Table: Users
DROP TABLE IF EXISTS `Users`;

CREATE TABLE `Users` (
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table `Users`
INSERT INTO `Users` (`email`, `first_name`, `last_name`) VALUES ('benporat3@mail.tau.ac.il', 'liron', 'benpo');
INSERT INTO `Users` (`email`, `first_name`, `last_name`) VALUES ('gabi@gmail.com', 'Gabi', 'Hameleh');
INSERT INTO `Users` (`email`, `first_name`, `last_name`) VALUES ('guest1@temp.com', 'Guest', 'One');
INSERT INTO `Users` (`email`, `first_name`, `last_name`) VALUES ('guest2@temp.com', 'Guest', 'Two');
INSERT INTO `Users` (`email`, `first_name`, `last_name`) VALUES ('lihibarmeir@mail.tau.ac.il', 'lihi', 'bar meir');
INSERT INTO `Users` (`email`, `first_name`, `last_name`) VALUES ('noyastorzi@mail.tau.ac.il', 'noya', 'storzi');
INSERT INTO `Users` (`email`, `first_name`, `last_name`) VALUES ('ortalleviron@mail.tau.ac.il', 'ortal', 'levi ron');
INSERT INTO `Users` (`email`, `first_name`, `last_name`) VALUES ('reg1@gmail.com', 'John', 'Doe');
INSERT INTO `Users` (`email`, `first_name`, `last_name`) VALUES ('reg2@yahoo.com', 'Jane', 'Smith');

SET FOREIGN_KEY_CHECKS=1;