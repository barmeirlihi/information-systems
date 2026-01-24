-- FlyTau Database Population Script
-- Adds 10 airports, 90 routes, flights, orders, and tickets

-- ============================================
-- 1. ADD AIRPORTS (6 additional airports)
-- ============================================
INSERT INTO Airports (airport_name, country, city) VALUES 
('DXB', 'UAE', 'Dubai'),
('FRA', 'Germany', 'Frankfurt'),
('IST', 'Turkey', 'Istanbul'),
('MAD', 'Spain', 'Madrid'),
('AMS', 'Netherlands', 'Amsterdam'),
('BCN', 'Spain', 'Barcelona')
ON DUPLICATE KEY UPDATE airport_name=airport_name;

-- ============================================
-- 2. CREATE ROUTES (from every airport to every other airport)
-- Total: 10 airports * 9 destinations = 90 routes
-- ============================================

-- TLV routes (to all other airports)
INSERT INTO FlightRoutes (origin_airport_name, destination_airport_name, flight_duration) VALUES
('TLV', 'JFK', 720), ('TLV', 'LHR', 300), ('TLV', 'CDG', 270), ('TLV', 'DXB', 180),
('TLV', 'FRA', 240), ('TLV', 'IST', 120), ('TLV', 'MAD', 300), ('TLV', 'AMS', 300), ('TLV', 'BCN', 300)
ON DUPLICATE KEY UPDATE flight_duration=VALUES(flight_duration);

-- JFK routes
INSERT INTO FlightRoutes (origin_airport_name, destination_airport_name, flight_duration) VALUES
('JFK', 'TLV', 660), ('JFK', 'LHR', 420), ('JFK', 'CDG', 420), ('JFK', 'DXB', 780),
('JFK', 'FRA', 420), ('JFK', 'IST', 600), ('JFK', 'MAD', 420), ('JFK', 'AMS', 420), ('JFK', 'BCN', 420)
ON DUPLICATE KEY UPDATE flight_duration=VALUES(flight_duration);

-- LHR routes
INSERT INTO FlightRoutes (origin_airport_name, destination_airport_name, flight_duration) VALUES
('LHR', 'TLV', 300), ('LHR', 'JFK', 420), ('LHR', 'CDG', 90), ('LHR', 'DXB', 360),
('LHR', 'FRA', 90), ('LHR', 'IST', 240), ('LHR', 'MAD', 150), ('LHR', 'AMS', 60), ('LHR', 'BCN', 120)
ON DUPLICATE KEY UPDATE flight_duration=VALUES(flight_duration);

-- CDG routes
INSERT INTO FlightRoutes (origin_airport_name, destination_airport_name, flight_duration) VALUES
('CDG', 'TLV', 270), ('CDG', 'JFK', 420), ('CDG', 'LHR', 90), ('CDG', 'DXB', 360),
('CDG', 'FRA', 60), ('CDG', 'IST', 210), ('CDG', 'MAD', 120), ('CDG', 'AMS', 60), ('CDG', 'BCN', 90)
ON DUPLICATE KEY UPDATE flight_duration=VALUES(flight_duration);

-- DXB routes
INSERT INTO FlightRoutes (origin_airport_name, destination_airport_name, flight_duration) VALUES
('DXB', 'TLV', 180), ('DXB', 'JFK', 780), ('DXB', 'LHR', 360), ('DXB', 'CDG', 360),
('DXB', 'FRA', 300), ('DXB', 'IST', 180), ('DXB', 'MAD', 360), ('DXB', 'AMS', 360), ('DXB', 'BCN', 360)
ON DUPLICATE KEY UPDATE flight_duration=VALUES(flight_duration);

-- FRA routes
INSERT INTO FlightRoutes (origin_airport_name, destination_airport_name, flight_duration) VALUES
('FRA', 'TLV', 240), ('FRA', 'JFK', 420), ('FRA', 'LHR', 90), ('FRA', 'CDG', 60),
('FRA', 'DXB', 300), ('FRA', 'IST', 180), ('FRA', 'MAD', 120), ('FRA', 'AMS', 60), ('FRA', 'BCN', 90)
ON DUPLICATE KEY UPDATE flight_duration=VALUES(flight_duration);

-- IST routes
INSERT INTO FlightRoutes (origin_airport_name, destination_airport_name, flight_duration) VALUES
('IST', 'TLV', 120), ('IST', 'JFK', 600), ('IST', 'LHR', 240), ('IST', 'CDG', 210),
('IST', 'DXB', 180), ('IST', 'FRA', 180), ('IST', 'MAD', 240), ('IST', 'AMS', 210), ('IST', 'BCN', 210)
ON DUPLICATE KEY UPDATE flight_duration=VALUES(flight_duration);

-- MAD routes
INSERT INTO FlightRoutes (origin_airport_name, destination_airport_name, flight_duration) VALUES
('MAD', 'TLV', 300), ('MAD', 'JFK', 420), ('MAD', 'LHR', 150), ('MAD', 'CDG', 120),
('MAD', 'DXB', 360), ('MAD', 'FRA', 120), ('MAD', 'IST', 240), ('MAD', 'AMS', 120), ('MAD', 'BCN', 60)
ON DUPLICATE KEY UPDATE flight_duration=VALUES(flight_duration);

-- AMS routes
INSERT INTO FlightRoutes (origin_airport_name, destination_airport_name, flight_duration) VALUES
('AMS', 'TLV', 300), ('AMS', 'JFK', 420), ('AMS', 'LHR', 60), ('AMS', 'CDG', 60),
('AMS', 'DXB', 360), ('AMS', 'FRA', 60), ('AMS', 'IST', 210), ('AMS', 'MAD', 120), ('AMS', 'BCN', 120)
ON DUPLICATE KEY UPDATE flight_duration=VALUES(flight_duration);

-- BCN routes
INSERT INTO FlightRoutes (origin_airport_name, destination_airport_name, flight_duration) VALUES
('BCN', 'TLV', 300), ('BCN', 'JFK', 420), ('BCN', 'LHR', 120), ('BCN', 'CDG', 90),
('BCN', 'DXB', 360), ('BCN', 'FRA', 90), ('BCN', 'IST', 210), ('BCN', 'MAD', 60), ('BCN', 'AMS', 120)
ON DUPLICATE KEY UPDATE flight_duration=VALUES(flight_duration);

-- ============================================
-- 3. ADD FLIGHTS (with different statuses and dates)
-- ============================================

-- Active flights (future dates)
INSERT INTO Flights (flight_id, departure_time, departure_date, status, plane_id, origin_airport_name, destination_airport_name, price_economy, price_business) VALUES
-- TLV flights
(2001, '08:00:00', '2026-02-15', 'Active', 1, 'TLV', 'JFK', 650.00, 1300.00),
(2002, '14:30:00', '2026-02-16', 'Active', 2, 'TLV', 'LHR', 320.00, NULL),
(2003, '10:15:00', '2026-02-17', 'Active', 3, 'TLV', 'CDG', 280.00, 560.00),
(2004, '16:00:00', '2026-02-18', 'Active', 1, 'TLV', 'DXB', 200.00, 400.00),
(2005, '12:00:00', '2026-02-19', 'Active', 2, 'TLV', 'FRA', 300.00, NULL),
(2006, '09:30:00', '2026-02-20', 'Active', 3, 'TLV', 'IST', 150.00, 300.00),
(2007, '11:00:00', '2026-02-21', 'Active', 1, 'TLV', 'MAD', 350.00, 700.00),
(2008, '13:45:00', '2026-02-22', 'Active', 2, 'TLV', 'AMS', 330.00, NULL),
(2009, '15:20:00', '2026-02-23', 'Active', 3, 'TLV', 'BCN', 340.00, 680.00),

-- JFK flights
(2010, '22:00:00', '2026-02-15', 'Active', 1, 'JFK', 'TLV', 750.00, 1500.00),
(2011, '20:30:00', '2026-02-16', 'Active', 1, 'JFK', 'LHR', 500.00, 1000.00),
(2012, '21:00:00', '2026-02-17', 'Active', 1, 'JFK', 'CDG', 520.00, 1040.00),
(2013, '19:00:00', '2026-02-18', 'Active', 1, 'JFK', 'DXB', 850.00, 1700.00),
(2014, '20:00:00', '2026-02-19', 'Active', 1, 'JFK', 'FRA', 510.00, 1020.00),
(2015, '18:30:00', '2026-02-20', 'Active', 1, 'JFK', 'IST', 720.00, 1440.00),
(2016, '21:30:00', '2026-02-21', 'Active', 1, 'JFK', 'MAD', 530.00, 1060.00),
(2017, '19:30:00', '2026-02-22', 'Active', 1, 'JFK', 'AMS', 515.00, 1030.00),
(2018, '22:30:00', '2026-02-23', 'Active', 1, 'JFK', 'BCN', 525.00, 1050.00),

-- LHR flights
(2019, '09:00:00', '2026-02-15', 'Active', 2, 'LHR', 'TLV', 310.00, NULL),
(2020, '10:30:00', '2026-02-16', 'Active', 1, 'LHR', 'JFK', 490.00, 980.00),
(2021, '08:15:00', '2026-02-17', 'Active', 2, 'LHR', 'CDG', 100.00, NULL),
(2022, '11:00:00', '2026-02-18', 'Active', 1, 'LHR', 'DXB', 380.00, 760.00),
(2023, '09:45:00', '2026-02-19', 'Active', 2, 'LHR', 'FRA', 95.00, NULL),
(2024, '12:30:00', '2026-02-20', 'Active', 1, 'LHR', 'IST', 250.00, 500.00),
(2025, '10:00:00', '2026-02-21', 'Active', 2, 'LHR', 'MAD', 160.00, NULL),
(2026, '08:30:00', '2026-02-22', 'Active', 2, 'LHR', 'AMS', 70.00, NULL),
(2027, '11:30:00', '2026-02-23', 'Active', 2, 'LHR', 'BCN', 130.00, NULL),

-- CDG flights
(2028, '10:00:00', '2026-02-15', 'Active', 3, 'CDG', 'TLV', 275.00, 550.00),
(2029, '21:00:00', '2026-02-16', 'Active', 1, 'CDG', 'JFK', 510.00, 1020.00),
(2030, '08:00:00', '2026-02-17', 'Active', 2, 'CDG', 'LHR', 95.00, NULL),
(2031, '14:00:00', '2026-02-18', 'Active', 1, 'CDG', 'DXB', 370.00, 740.00),
(2032, '09:30:00', '2026-02-19', 'Active', 2, 'CDG', 'FRA', 65.00, NULL),
(2033, '12:00:00', '2026-02-20', 'Active', 3, 'CDG', 'IST', 220.00, 440.00),
(2034, '11:00:00', '2026-02-21', 'Active', 2, 'CDG', 'MAD', 125.00, NULL),
(2035, '13:00:00', '2026-02-22', 'Active', 2, 'CDG', 'AMS', 65.00, NULL),
(2036, '15:00:00', '2026-02-23', 'Active', 2, 'CDG', 'BCN', 95.00, NULL);

-- Landed flights (past dates)
INSERT INTO Flights (flight_id, departure_time, departure_date, status, plane_id, origin_airport_name, destination_airport_name, price_economy, price_business) VALUES
-- TLV flights (past)
(2101, '08:00:00', '2025-08-15', 'Landed', 1, 'TLV', 'JFK', 600.00, 1200.00),
(2102, '14:30:00', '2025-08-16', 'Landed', 2, 'TLV', 'LHR', 300.00, NULL),
(2103, '10:15:00', '2025-08-17', 'Landed', 3, 'TLV', 'CDG', 270.00, 540.00),
(2104, '16:00:00', '2025-08-18', 'Landed', 1, 'TLV', 'DXB', 180.00, 360.00),
(2105, '12:00:00', '2025-08-19', 'Landed', 2, 'TLV', 'FRA', 240.00, NULL),
(2106, '09:30:00', '2025-08-20', 'Landed', 3, 'TLV', 'IST', 120.00, 240.00),
(2107, '11:00:00', '2025-08-21', 'Landed', 1, 'TLV', 'MAD', 300.00, 600.00),
(2108, '13:45:00', '2025-08-22', 'Landed', 2, 'TLV', 'AMS', 300.00, NULL),
(2109, '15:20:00', '2025-08-23', 'Landed', 3, 'TLV', 'BCN', 300.00, 600.00),

-- JFK flights (past)
(2110, '22:00:00', '2025-08-15', 'Landed', 1, 'JFK', 'TLV', 700.00, 1400.00),
(2111, '20:30:00', '2025-08-16', 'Landed', 1, 'JFK', 'LHR', 480.00, 960.00),
(2112, '21:00:00', '2025-08-17', 'Landed', 1, 'JFK', 'CDG', 500.00, 1000.00),
(2113, '19:00:00', '2025-08-18', 'Landed', 1, 'JFK', 'DXB', 800.00, 1600.00),
(2114, '20:00:00', '2025-08-19', 'Landed', 1, 'JFK', 'FRA', 490.00, 980.00),
(2115, '18:30:00', '2025-08-20', 'Landed', 1, 'JFK', 'IST', 700.00, 1400.00),
(2116, '21:30:00', '2025-08-21', 'Landed', 1, 'JFK', 'MAD', 510.00, 1020.00),
(2117, '19:30:00', '2025-08-22', 'Landed', 1, 'JFK', 'AMS', 495.00, 990.00),
(2118, '22:30:00', '2025-08-23', 'Landed', 1, 'JFK', 'BCN', 505.00, 1010.00),

-- LHR flights (past)
(2119, '09:00:00', '2025-08-15', 'Landed', 2, 'LHR', 'TLV', 290.00, NULL),
(2120, '10:30:00', '2025-08-16', 'Landed', 1, 'LHR', 'JFK', 470.00, 940.00),
(2121, '08:15:00', '2025-08-17', 'Landed', 2, 'LHR', 'CDG', 90.00, NULL),
(2122, '11:00:00', '2025-08-18', 'Landed', 1, 'LHR', 'DXB', 360.00, 720.00),
(2123, '09:45:00', '2025-08-19', 'Landed', 2, 'LHR', 'FRA', 85.00, NULL),
(2124, '12:30:00', '2025-08-20', 'Landed', 1, 'LHR', 'IST', 240.00, 480.00),
(2125, '10:00:00', '2025-08-21', 'Landed', 2, 'LHR', 'MAD', 150.00, NULL),
(2126, '08:30:00', '2025-08-22', 'Landed', 2, 'LHR', 'AMS', 60.00, NULL),
(2127, '11:30:00', '2025-08-23', 'Landed', 2, 'LHR', 'BCN', 120.00, NULL),

-- CDG flights (past)
(2128, '10:00:00', '2025-08-15', 'Landed', 3, 'CDG', 'TLV', 265.00, 530.00),
(2129, '21:00:00', '2025-08-16', 'Landed', 1, 'CDG', 'JFK', 500.00, 1000.00),
(2130, '08:00:00', '2025-08-17', 'Landed', 2, 'CDG', 'LHR', 85.00, NULL),
(2131, '14:00:00', '2025-08-18', 'Landed', 1, 'CDG', 'DXB', 350.00, 700.00),
(2132, '09:30:00', '2025-08-19', 'Landed', 2, 'CDG', 'FRA', 55.00, NULL),
(2133, '12:00:00', '2025-08-20', 'Landed', 3, 'CDG', 'IST', 210.00, 420.00),
(2134, '11:00:00', '2025-08-21', 'Landed', 2, 'CDG', 'MAD', 115.00, NULL),
(2135, '13:00:00', '2025-08-22', 'Landed', 2, 'CDG', 'AMS', 55.00, NULL),
(2136, '15:00:00', '2025-08-23', 'Landed', 2, 'CDG', 'BCN', 85.00, NULL);

-- Cancelled flights
INSERT INTO Flights (flight_id, departure_time, departure_date, status, plane_id, origin_airport_name, destination_airport_name, price_economy, price_business) VALUES
(2201, '08:00:00', '2025-09-01', 'Cancelled', 1, 'TLV', 'JFK', 600.00, 1200.00),
(2202, '14:30:00', '2025-09-02', 'Cancelled', 2, 'TLV', 'LHR', 300.00, NULL),
(2203, '10:15:00', '2026-03-01', 'Cancelled', 3, 'TLV', 'CDG', 280.00, 560.00),
(2204, '16:00:00', '2026-03-02', 'Cancelled', 1, 'TLV', 'DXB', 200.00, 400.00),
(2205, '12:00:00', '2025-09-05', 'Cancelled', 2, 'JFK', 'TLV', 700.00, 1400.00),
(2206, '20:30:00', '2026-03-03', 'Cancelled', 1, 'JFK', 'LHR', 500.00, 1000.00),
(2207, '09:00:00', '2025-09-10', 'Cancelled', 2, 'LHR', 'TLV', 290.00, NULL),
(2208, '10:00:00', '2026-03-04', 'Cancelled', 3, 'CDG', 'TLV', 275.00, 550.00);

-- ============================================
-- 4. ASSIGN CREW TO FLIGHTS
-- ============================================

-- Assign pilots to flights (2 pilots for Small planes, 3 for Large)
-- Large planes (flight_id 2001, 2004, 2007, 2010-2018, etc.)
INSERT INTO Pilots_In_Flights (pilot_id, flight_id) VALUES
-- Flight 2001 (Large plane - TLV to JFK)
('200000001', 2001), ('200000002', 2001), ('200000004', 2001),
-- Flight 2004 (Large plane - TLV to DXB)
('200000001', 2004), ('200000002', 2004), ('200000006', 2004),
-- Flight 2007 (Large plane - TLV to MAD)
('200000002', 2007), ('200000004', 2007), ('200000008', 2007),
-- Flight 2010 (Large plane - JFK to TLV)
('200000001', 2010), ('200000002', 2010), ('200000004', 2010),
-- Flight 2011 (Large plane - JFK to LHR)
('200000002', 2011), ('200000004', 2011), ('200000006', 2011),
-- Flight 2012 (Large plane - JFK to CDG)
('200000001', 2012), ('200000004', 2012), ('200000008', 2012),
-- Flight 2013 (Large plane - JFK to DXB)
('200000002', 2013), ('200000006', 2013), ('200000008', 2013),
-- Flight 2014 (Large plane - JFK to FRA)
('200000001', 2014), ('200000002', 2014), ('200000010', 2014),
-- Flight 2015 (Large plane - JFK to IST)
('200000004', 2015), ('200000006', 2015), ('200000008', 2015),
-- Flight 2016 (Large plane - JFK to MAD)
('200000001', 2016), ('200000002', 2016), ('200000010', 2016),
-- Flight 2017 (Large plane - JFK to AMS)
('200000002', 2017), ('200000004', 2017), ('200000006', 2017),
-- Flight 2018 (Large plane - JFK to BCN)
('200000001', 2018), ('200000004', 2018), ('200000008', 2018),
-- Flight 2020 (Large plane - LHR to JFK)
('200000002', 2020), ('200000004', 2020), ('200000006', 2020),
-- Flight 2022 (Large plane - LHR to DXB)
('200000001', 2022), ('200000004', 2022), ('200000008', 2022),
-- Flight 2024 (Large plane - LHR to IST)
('200000002', 2024), ('200000006', 2024), ('200000010', 2024),
-- Flight 2029 (Large plane - CDG to JFK)
('200000001', 2029), ('200000002', 2029), ('200000004', 2029),
-- Flight 2031 (Large plane - CDG to DXB)
('200000002', 2031), ('200000004', 2031), ('200000006', 2031),
-- Flight 2033 (Large plane - CDG to IST)
('200000001', 2033), ('200000004', 2033), ('200000008', 2033);

-- Small planes (2 pilots each)
INSERT INTO Pilots_In_Flights (pilot_id, flight_id) VALUES
-- Flight 2002 (Small plane)
('200000003', 2002), ('200000005', 2002),
-- Flight 2005 (Small plane)
('200000003', 2005), ('200000007', 2005),
-- Flight 2008 (Small plane)
('200000005', 2008), ('200000007', 2008),
-- Flight 2021 (Small plane)
('200000003', 2021), ('200000005', 2021),
-- Flight 2023 (Small plane)
('200000003', 2023), ('200000007', 2023),
-- Flight 2025 (Small plane)
('200000005', 2025), ('200000007', 2025),
-- Flight 2026 (Small plane)
('200000003', 2026), ('200000009', 2026),
-- Flight 2027 (Small plane)
('200000005', 2027), ('200000007', 2027),
-- Flight 2030 (Small plane)
('200000003', 2030), ('200000005', 2030),
-- Flight 2032 (Small plane)
('200000003', 2032), ('200000007', 2032),
-- Flight 2034 (Small plane)
('200000005', 2034), ('200000007', 2034),
-- Flight 2035 (Small plane)
('200000003', 2035), ('200000009', 2035),
-- Flight 2036 (Small plane)
('200000005', 2036), ('200000007', 2036);

-- Assign attendants to flights (3 for Small, 6 for Large)
-- Large planes (6 attendants each)
INSERT INTO Attendants_In_Flights (attendant_id, flight_id) VALUES
-- Flight 2001
('100000001', 2001), ('100000002', 2001), ('100000004', 2001), ('100000007', 2001), ('100000008', 2001), ('100000009', 2001),
-- Flight 2004
('100000001', 2004), ('100000002', 2004), ('100000010', 2004), ('100000012', 2004), ('100000013', 2004), ('100000015', 2004),
-- Flight 2007
('100000002', 2007), ('100000004', 2007), ('100000007', 2007), ('100000008', 2007), ('100000009', 2007), ('100000012', 2007),
-- Flight 2010
('100000001', 2010), ('100000002', 2010), ('100000004', 2010), ('100000008', 2010), ('100000009', 2010), ('100000010', 2010),
-- Flight 2011
('100000002', 2011), ('100000004', 2011), ('100000007', 2011), ('100000009', 2011), ('100000012', 2011), ('100000013', 2011),
-- Flight 2012
('100000001', 2012), ('100000004', 2012), ('100000007', 2012), ('100000008', 2012), ('100000010', 2012), ('100000015', 2012),
-- Flight 2013
('100000002', 2013), ('100000007', 2013), ('100000008', 2013), ('100000009', 2013), ('100000012', 2013), ('100000013', 2013),
-- Flight 2014
('100000001', 2014), ('100000002', 2014), ('100000004', 2014), ('100000009', 2014), ('100000010', 2014), ('100000015', 2014),
-- Flight 2015
('100000004', 2015), ('100000007', 2015), ('100000008', 2015), ('100000010', 2015), ('100000012', 2015), ('100000013', 2015),
-- Flight 2016
('100000001', 2016), ('100000002', 2016), ('100000004', 2016), ('100000007', 2016), ('100000009', 2016), ('100000015', 2016),
-- Flight 2017
('100000002', 2017), ('100000004', 2017), ('100000007', 2017), ('100000008', 2017), ('100000012', 2017), ('100000013', 2017),
-- Flight 2018
('100000001', 2018), ('100000004', 2018), ('100000007', 2018), ('100000008', 2018), ('100000009', 2018), ('100000010', 2018),
-- Flight 2020
('100000002', 2020), ('100000004', 2020), ('100000007', 2020), ('100000008', 2020), ('100000009', 2020), ('100000012', 2020),
-- Flight 2022
('100000001', 2022), ('100000004', 2022), ('100000007', 2022), ('100000008', 2022), ('100000010', 2022), ('100000015', 2022),
-- Flight 2024
('100000002', 2024), ('100000007', 2024), ('100000008', 2024), ('100000009', 2024), ('100000012', 2024), ('100000013', 2024),
-- Flight 2029
('100000001', 2029), ('100000002', 2029), ('100000004', 2029), ('100000008', 2029), ('100000009', 2029), ('100000010', 2029),
-- Flight 2031
('100000002', 2031), ('100000004', 2031), ('100000007', 2031), ('100000009', 2031), ('100000012', 2031), ('100000015', 2031),
-- Flight 2033
('100000001', 2033), ('100000004', 2033), ('100000007', 2033), ('100000008', 2033), ('100000010', 2033), ('100000013', 2033);

-- Small planes (3 attendants each)
INSERT INTO Attendants_In_Flights (attendant_id, flight_id) VALUES
-- Flight 2002
('100000003', 2002), ('100000005', 2002), ('100000006', 2002),
-- Flight 2005
('100000003', 2005), ('100000005', 2005), ('100000011', 2005),
-- Flight 2008
('100000005', 2008), ('100000006', 2008), ('100000011', 2008),
-- Flight 2021
('100000003', 2021), ('100000005', 2021), ('100000006', 2021),
-- Flight 2023
('100000003', 2023), ('100000005', 2023), ('100000011', 2023),
-- Flight 2025
('100000005', 2025), ('100000006', 2025), ('100000011', 2025),
-- Flight 2026
('100000003', 2026), ('100000005', 2026), ('100000014', 2026),
-- Flight 2027
('100000005', 2027), ('100000006', 2027), ('100000011', 2027),
-- Flight 2030
('100000003', 2030), ('100000005', 2030), ('100000006', 2030),
-- Flight 2032
('100000003', 2032), ('100000005', 2032), ('100000011', 2032),
-- Flight 2034
('100000005', 2034), ('100000006', 2034), ('100000011', 2034),
-- Flight 2035
('100000003', 2035), ('100000005', 2035), ('100000014', 2035),
-- Flight 2036
('100000005', 2036), ('100000006', 2036), ('100000011', 2036);

-- ============================================
-- 5. ADD ORDERS AND TICKETS
-- ============================================

-- Orders for landed flights
INSERT INTO Orders (order_id, email, order_status, order_date, total_payment) VALUES
(1001, 'reg1@gmail.com', 'Confirmed', '2025-07-15', 1200.00),
(1002, 'guest1@temp.com', 'Confirmed', '2025-07-16', 600.00),
(1003, 'reg2@yahoo.com', 'Confirmed', '2025-07-17', 540.00),
(1004, 'guest2@temp.com', 'Confirmed', '2025-07-18', 360.00),
(1005, 'reg1@gmail.com', 'Confirmed', '2025-07-19', 480.00),
(1006, 'guest1@temp.com', 'Confirmed', '2025-07-20', 240.00),
(1007, 'reg2@yahoo.com', 'Confirmed', '2025-07-21', 600.00),
(1008, 'guest2@temp.com', 'Confirmed', '2025-07-22', 600.00),
(1009, 'reg1@gmail.com', 'Confirmed', '2025-07-23', 600.00),
(1010, 'guest1@temp.com', 'Cancelled', '2025-07-15', 1400.00),
(1011, 'reg2@yahoo.com', 'Confirmed', '2025-07-16', 960.00),
(1012, 'guest2@temp.com', 'Confirmed', '2025-07-17', 1000.00),
(1013, 'reg1@gmail.com', 'Confirmed', '2025-07-18', 1600.00),
(1014, 'guest1@temp.com', 'Confirmed', '2025-07-19', 980.00),
(1015, 'reg2@yahoo.com', 'Cancelled', '2025-07-20', 1440.00),
(1016, 'guest2@temp.com', 'Confirmed', '2025-07-21', 1020.00),
(1017, 'reg1@gmail.com', 'Confirmed', '2025-07-22', 990.00),
(1018, 'guest1@temp.com', 'Confirmed', '2025-07-23', 1010.00),
(1019, 'reg2@yahoo.com', 'Confirmed', '2025-07-15', 290.00),
(1020, 'guest2@temp.com', 'Confirmed', '2025-07-16', 940.00),
(1021, 'reg1@gmail.com', 'Confirmed', '2025-07-17', 90.00),
(1022, 'guest1@temp.com', 'Confirmed', '2025-07-18', 720.00),
(1023, 'reg2@yahoo.com', 'Confirmed', '2025-07-19', 85.00),
(1024, 'guest2@temp.com', 'Confirmed', '2025-07-20', 480.00),
(1025, 'reg1@gmail.com', 'Confirmed', '2025-07-21', 150.00),
(1026, 'guest1@temp.com', 'Confirmed', '2025-07-22', 60.00),
(1027, 'reg2@yahoo.com', 'Confirmed', '2025-07-23', 120.00),
(1028, 'guest2@temp.com', 'Confirmed', '2025-07-15', 530.00),
(1029, 'reg1@gmail.com', 'Confirmed', '2025-07-16', 1000.00),
(1030, 'guest1@temp.com', 'Confirmed', '2025-07-17', 85.00),
(1031, 'reg2@yahoo.com', 'Confirmed', '2025-07-18', 700.00),
(1032, 'guest2@temp.com', 'Confirmed', '2025-07-19', 55.00),
(1033, 'reg1@gmail.com', 'Confirmed', '2025-07-20', 420.00),
(1034, 'guest1@temp.com', 'Confirmed', '2025-07-21', 115.00),
(1035, 'reg2@yahoo.com', 'Confirmed', '2025-07-22', 55.00),
(1036, 'guest2@temp.com', 'Confirmed', '2025-07-23', 85.00);

-- Flight tickets for orders
INSERT INTO FlightTickets (order_id, flight_id, plane_id, seat_row, seat_column) VALUES
-- Order 1001 (flight 2101 - TLV to JFK, Large plane)
(1001, 2101, 1, 1, 'A'), (1001, 2101, 1, 1, 'B'),
-- Order 1002 (flight 2102 - TLV to LHR, Small plane)
(1002, 2102, 2, 1, 'A'),
-- Order 1003 (flight 2103 - TLV to CDG, Large plane)
(1003, 2103, 3, 2, 'A'), (1003, 2103, 3, 2, 'B'),
-- Order 1004 (flight 2104 - TLV to DXB, Large plane)
(1004, 2104, 1, 3, 'A'),
-- Order 1005 (flight 2105 - TLV to FRA, Small plane)
(1005, 2105, 2, 1, 'B'), (1005, 2105, 2, 1, 'C'),
-- Order 1006 (flight 2106 - TLV to IST, Large plane)
(1006, 2106, 3, 4, 'A'),
-- Order 1007 (flight 2107 - TLV to MAD, Large plane)
(1007, 2107, 1, 2, 'A'), (1007, 2107, 1, 2, 'B'),
-- Order 1008 (flight 2108 - TLV to AMS, Small plane)
(1008, 2108, 2, 2, 'A'),
-- Order 1009 (flight 2109 - TLV to BCN, Large plane)
(1009, 2109, 3, 5, 'A'),
-- Order 1010 (flight 2110 - JFK to TLV, Large plane)
(1010, 2110, 1, 1, 'A'), (1010, 2110, 1, 1, 'B'),
-- Order 1011 (flight 2111 - JFK to LHR, Large plane)
(1011, 2111, 1, 2, 'A'),
-- Order 1012 (flight 2112 - JFK to CDG, Large plane)
(1012, 2112, 1, 3, 'A'), (1012, 2112, 1, 3, 'B'),
-- Order 1013 (flight 2113 - JFK to DXB, Large plane)
(1013, 2113, 1, 4, 'A'),
-- Order 1014 (flight 2114 - JFK to FRA, Large plane)
(1014, 2114, 1, 2, 'B'), (1014, 2114, 1, 2, 'C'),
-- Order 1015 (flight 2115 - JFK to IST, Large plane)
(1015, 2115, 1, 5, 'A'),
-- Order 1016 (flight 2116 - JFK to MAD, Large plane)
(1016, 2116, 1, 3, 'C'), (1016, 2116, 1, 3, 'D'),
-- Order 1017 (flight 2117 - JFK to AMS, Large plane)
(1017, 2117, 1, 4, 'B'),
-- Order 1018 (flight 2118 - JFK to BCN, Large plane)
(1018, 2118, 1, 6, 'A'),
-- Order 1019 (flight 2119 - LHR to TLV, Small plane)
(1019, 2119, 2, 1, 'A'),
-- Order 1020 (flight 2120 - LHR to JFK, Large plane)
(1020, 2120, 1, 1, 'C'), (1020, 2120, 1, 1, 'D'),
-- Order 1021 (flight 2121 - LHR to CDG, Small plane)
(1021, 2121, 2, 2, 'B'),
-- Order 1022 (flight 2122 - LHR to DXB, Large plane)
(1022, 2122, 1, 7, 'A'),
-- Order 1023 (flight 2123 - LHR to FRA, Small plane)
(1023, 2123, 2, 3, 'A'),
-- Order 1024 (flight 2124 - LHR to IST, Large plane)
(1024, 2124, 1, 2, 'D'),
-- Order 1025 (flight 2125 - LHR to MAD, Small plane)
(1025, 2125, 2, 1, 'C'),
-- Order 1026 (flight 2126 - LHR to AMS, Small plane)
(1026, 2126, 2, 2, 'C'),
-- Order 1027 (flight 2127 - LHR to BCN, Small plane)
(1027, 2127, 2, 3, 'B'),
-- Order 1028 (flight 2128 - CDG to TLV, Large plane)
(1028, 2128, 3, 1, 'A'), (1028, 2128, 3, 1, 'B'),
-- Order 1029 (flight 2129 - CDG to JFK, Large plane)
(1029, 2129, 1, 8, 'A'),
-- Order 1030 (flight 2130 - CDG to LHR, Small plane)
(1030, 2130, 2, 4, 'A'),
-- Order 1031 (flight 2131 - CDG to DXB, Large plane)
(1031, 2131, 1, 3, 'E'), (1031, 2131, 1, 3, 'F'),
-- Order 1032 (flight 2132 - CDG to FRA, Small plane)
(1032, 2132, 2, 1, 'D'),
-- Order 1033 (flight 2133 - CDG to IST, Large plane)
(1033, 2133, 3, 2, 'C'),
-- Order 1034 (flight 2134 - CDG to MAD, Small plane)
(1034, 2134, 2, 2, 'D'),
-- Order 1035 (flight 2135 - CDG to AMS, Small plane)
(1035, 2135, 2, 3, 'C'),
-- Order 1036 (flight 2136 - CDG to BCN, Small plane)
(1036, 2136, 2, 4, 'B');

-- ============================================
-- END OF POPULATION SCRIPT
-- ============================================

