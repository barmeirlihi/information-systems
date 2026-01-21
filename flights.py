import data
from datetime import datetime, date
from abc import ABC, abstractmethod


class Seat:
    """Represents a single seat on a plane"""
    
    def __init__(self, plane_id, row, column, seat_class):
        self.plane_id = plane_id
        self.row = row
        self.column = column
        self.seat_class = seat_class  # 'Economy' or 'Business'
    
    def __repr__(self):
        return f"Seat({self.row}-{self.column}, {self.seat_class})"
    
    def get_seat_key(self):
        """Returns tuple (row, column) for seat identification"""
        return (self.row, self.column)
    
    @staticmethod
    def get_seats_for_plane(plane_id):
        """Static method to get all seats for a plane from database"""
        query = """
            SELECT seat_row, seat_column, seat_class
            FROM Seats
            WHERE plane_id = %s
            ORDER BY seat_row, seat_column
        """
        result = data.sql_query(query, plane_id)
        return [Seat(plane_id, row[0], row[1], row[2]) for row in result]


class Flight(ABC):
    """Abstract base class for flights"""
    
    def __init__(self, flight_id, departure_time, departure_date, status, 
                 plane_id, origin_airport, destination_airport, 
                 price_economy, price_business=None, 
                 origin_city=None, origin_country=None,
                 destination_city=None, destination_country=None,
                 flight_duration=None):
        self.flight_id = flight_id
        self.departure_time = departure_time
        self.departure_date = departure_date
        self.status = status
        self.plane_id = plane_id
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.price_economy = float(price_economy) if price_economy is not None else 0.0
        self.price_business = float(price_business) if price_business is not None else None
        self.origin_city = origin_city
        self.origin_country = origin_country
        self.destination_city = destination_city
        self.destination_country = destination_country
        self.flight_duration = flight_duration
        self._seats = None
        self._booked_seats = None
    
    @abstractmethod
    def get_plane_size(self):
        """Returns the size of the plane ('Small' or 'Large')"""
        pass
    
    def get_seats(self):
        """Lazy loading of seats - loads from database if not already loaded"""
        if self._seats is None:
            self._seats = Seat.get_seats_for_plane(self.plane_id)
        return self._seats
    
    def get_booked_seats(self):
        """Gets set of booked seats for this flight"""
        if self._booked_seats is None:
            query = """
                SELECT seat_row, seat_column
                FROM FlightTickets
                WHERE flight_id = %s
            """
            result = data.sql_query(query, self.flight_id)
            self._booked_seats = set((row[0], row[1]) for row in result)
        return self._booked_seats
    
    def is_seat_available(self, row, column):
        """Checks if a specific seat is available"""
        return (row, column) not in self.get_booked_seats()
    
    def get_seat_by_position(self, row, column):
        """Gets a Seat object by row and column"""
        for seat in self.get_seats():
            if seat.row == row and seat.column == column:
                return seat
        return None
    
    def calculate_seat_price(self, seat):
        """Calculates the price for a specific seat"""
        if seat.seat_class == 'Business':
            if self.price_business is None:
                return None
            return self.price_business
        return self.price_economy
    
    def organize_seats_by_row(self):
        """Organizes seats by row and marks which are booked"""
        seats = self.get_seats()
        booked_seats = self.get_booked_seats()
        
        seats_by_row = {}
        for seat in seats:
            if seat.row not in seats_by_row:
                seats_by_row[seat.row] = []
            is_booked = seat.get_seat_key() in booked_seats
            seats_by_row[seat.row].append({
                'column': seat.column,
                'class': seat.seat_class,
                'booked': is_booked
            })
        
        # Sort seats by column within each row
        for row in seats_by_row:
            seats_by_row[row].sort(key=lambda x: x['column'])
        
        return seats_by_row
    
    def get_available_seats_count(self):
        """Returns the number of available seats"""
        total_seats = len(self.get_seats())
        booked_seats = len(self.get_booked_seats())
        return total_seats - booked_seats
    
    def validate_seat_selection(self, selected_seats):
        """
        Validates selected seats and calculates total price
        Returns: (total_price, seat_details, error_message)
        """
        booked_seats = self.get_booked_seats()
        total_price = 0
        seat_details = []
        
        for seat_str in selected_seats:
            parts = seat_str.split('-')
            if len(parts) != 2:
                return None, None, "Invalid seat format"
            
            try:
                seat_row = int(parts[0])
                seat_column = int(parts[1])
            except ValueError:
                return None, None, "Invalid seat numbers"
            
            # Check if seat is still available
            if not self.is_seat_available(seat_row, seat_column):
                return None, None, "One or more selected seats are no longer available"
            
            # Get seat object
            seat = self.get_seat_by_position(seat_row, seat_column)
            if seat is None:
                return None, None, f"Seat {seat_row}-{seat_column} not found"
            
            # Calculate price
            price = self.calculate_seat_price(seat)
            if price is None:
                if seat.seat_class == 'Business':
                    return None, None, "Business class seats are not available for this flight"
                else:
                    return None, None, f"Seat {seat_row}-{seat_column} has invalid pricing"
            
            total_price += price
            seat_details.append((seat_row, seat_column, seat.seat_class))
        
        return total_price, seat_details, None
    
    def book_seats(self, order_id, seat_details):
        """Books multiple seats for this flight"""
        for seat_row, seat_column, seat_class in seat_details:
            query = """
                INSERT INTO FlightTickets (order_id, flight_id, plane_id, seat_row, seat_column)
                VALUES (%s, %s, %s, %s, %s)
            """
            data.sql_insert(query, order_id, self.flight_id, self.plane_id, 
                          seat_row, seat_column)
        # Clear cached booked seats to force refresh
        self._booked_seats = None
    
    def cancel_order_seats(self, order_id):
        """
        Cancels seats for a specific order (frees up seats)
        
        Args:
            order_id: Order ID to cancel seats for
        """
        query = """
            DELETE FROM FlightTickets
            WHERE order_id = %s AND flight_id = %s
        """
        data.sql_insert(query, order_id, self.flight_id)
        # Clear cached booked seats to force refresh
        self._booked_seats = None
    
    def cancel_flight(self):
        """
        Cancels the flight - updates status to 'Cancelled'
        Also updates all related orders to 'Cancelled by System' and sets total_payment to 0
        (full refund for customers)
        
        Returns:
            (success, error_message)
        """
        try:
            # Update flight status
            query = """
                UPDATE Flights
                SET status = 'Cancelled'
                WHERE flight_id = %s
            """
            data.sql_insert(query, self.flight_id)
            self.status = 'Cancelled'
            
            # Update all orders for this flight to 'Cancelled by System' and set total_payment to 0 (full refund)
            orders_query = """
                UPDATE Orders
                SET order_status = 'Cancelled by System',
                    total_payment = 0.0
                WHERE order_id IN (
                    SELECT DISTINCT order_id
                    FROM FlightTickets
                    WHERE flight_id = %s
                )
            """
            data.sql_insert(orders_query, self.flight_id)
            
            return True, None
        except Exception as e:
            return False, f"Error cancelling flight: {str(e)}"
    
    def get_destination_image(self):
        """Returns URL of destination image"""
        destination_images = {
            'TLV': 'https://www.atarim.gov.il/wp-content/uploads/2020/06/Screenshot_1.png',
            'JFK': 'https://www.masa.co.il/wp-content/uploads/2017/10/nyc_open.jpg',
            'LHR': 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&q=80&w=800',
            'CDG': 'https://www.gotravel.co.il/userfiles/_big_BEF155E213C8181A3435EF4084F79D94.jpg',
            'DXB': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&q=80&w=800',
            'FRA': 'https://images.unsplash.com/photo-1556388158-158ea5ccacbd?auto=format&fit=crop&q=80&w=800',
            'IST': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&q=80&w=800',
            'MAD': 'https://images.unsplash.com/photo-1539037116277-4db20889f2d4?auto=format&fit=crop&q=80&w=800',
            'AMS': 'https://www.elal.com/magazine/wp-content/uploads/2019/04/shutterstock_797232592.jpg',
            'BCN': 'https://images.unsplash.com/photo-1539037116277-4db20889f2d4?auto=format&fit=crop&q=80&w=800',
            'BKK': 'https://www.elal.com/magazine/wp-content/uploads/2017/01/ThinkstockPhotos-480903890.jpg',
            'FCO': 'https://www.in-italy.co.il/upload1/rome1.jpg',
            'NRT': 'https://www.elal.com/magazine/wp-content/uploads/2019/11/shutterstock_1030169917.jpg',
            'HND': 'https://www.elal.com/magazine/wp-content/uploads/2019/11/shutterstock_1030169917.jpg',
        }
        default_image = 'https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&q=80&w=800'
        return destination_images.get(self.destination_airport, default_image)
    
    @staticmethod
    def get_flight_by_id(flight_id, include_all_statuses=False):
        """
        Factory method to create appropriate Flight subclass from database
        
        Args:
            flight_id: Flight ID
            include_all_statuses: If True, includes all flights regardless of status.
                                 If False, only returns Active flights.
        """
        query = """
            SELECT 
                f.flight_id,
                f.departure_time,
                f.departure_date,
                f.status,
                f.plane_id,
                f.origin_airport_name,
                f.destination_airport_name,
                f.price_economy,
                f.price_business,
                ao.city as origin_city,
                ao.country as origin_country,
                ad.city as destination_city,
                ad.country as destination_country,
                p.size as plane_size
            FROM Flights f
            JOIN Airports ao ON f.origin_airport_name = ao.airport_name
            JOIN Airports ad ON f.destination_airport_name = ad.airport_name
            JOIN Planes p ON f.plane_id = p.plane_id
            WHERE f.flight_id = %s
        """
        if not include_all_statuses:
            query += " AND f.status = 'Active'"
        
        result = data.sql_query(query, flight_id)
        if not result:
            return None
        
        row = result[0]
        plane_size = row[13]  # plane_size
        
        # Get flight duration
        duration_query = """
            SELECT flight_duration
            FROM FlightRoutes
            WHERE origin_airport_name = %s AND destination_airport_name = %s
        """
        duration_result = data.sql_query(duration_query, row[5], row[6])
        flight_duration = duration_result[0][0] if duration_result else None
        
        if plane_size == 'Small':
            return SmallFlight(
                flight_id=row[0],
                departure_time=row[1],
                departure_date=row[2],
                status=row[3],
                plane_id=row[4],
                origin_airport=row[5],
                destination_airport=row[6],
                price_economy=row[7],
                price_business=row[8],
                origin_city=row[9],
                origin_country=row[10],
                destination_city=row[11],
                destination_country=row[12],
                flight_duration=flight_duration
            )
        else:  # Large
            return LargeFlight(
                flight_id=row[0],
                departure_time=row[1],
                departure_date=row[2],
                status=row[3],
                plane_id=row[4],
                origin_airport=row[5],
                destination_airport=row[6],
                price_economy=row[7],
                price_business=row[8],
                origin_city=row[9],
                origin_country=row[10],
                destination_city=row[11],
                destination_country=row[12],
                flight_duration=flight_duration
            )
    
    @staticmethod
    def get_active_flights(origin=None, destination=None, flight_date=None):
        """Gets list of active flights, returns as list of Flight objects"""
        query = """
            SELECT 
                f.flight_id,
                f.departure_time,
                f.departure_date,
                f.origin_airport_name,
                f.destination_airport_name,
                f.price_economy,
                f.price_business,
                fr.flight_duration,
                ao.city as origin_city,
                ao.country as origin_country,
                ad.city as destination_city,
                ad.country as destination_country,
                f.plane_id,
                p.size as plane_size,
                (SELECT COUNT(*) FROM Seats s WHERE s.plane_id = f.plane_id) - 
                (SELECT COUNT(*) FROM FlightTickets ft WHERE ft.flight_id = f.flight_id) as available_seats
            FROM Flights f
            JOIN FlightRoutes fr ON f.origin_airport_name = fr.origin_airport_name 
                AND f.destination_airport_name = fr.destination_airport_name
            JOIN Airports ao ON f.origin_airport_name = ao.airport_name
            JOIN Airports ad ON f.destination_airport_name = ad.airport_name
            JOIN Planes p ON f.plane_id = p.plane_id
            WHERE f.status = 'Active'
        """
        
        params = []
        
        if origin:
            query += " AND f.origin_airport_name = %s"
            params.append(origin)
        
        if destination:
            query += " AND f.destination_airport_name = %s"
            params.append(destination)
        
        if flight_date:
            query += " AND f.departure_date = %s"
            params.append(flight_date)
        
        query += " ORDER BY f.departure_date, f.departure_time"
        
        result = data.sql_query(query, *params)
        flights = []
        
        for row in result:
            if row[13] == 'Small':  # plane_size
                flight = SmallFlight(
                    flight_id=row[0],
                    departure_time=row[1],
                    departure_date=row[2],
                    status='Active',
                    plane_id=row[12],
                    origin_airport=row[3],
                    destination_airport=row[4],
                    price_economy=row[5],
                    price_business=row[6],
                    origin_city=row[8],
                    origin_country=row[9],
                    destination_city=row[10],
                    destination_country=row[11],
                    flight_duration=row[7]
                )
            else:  # Large
                flight = LargeFlight(
                    flight_id=row[0],
                    departure_time=row[1],
                    departure_date=row[2],
                    status='Active',
                    plane_id=row[12],
                    origin_airport=row[3],
                    destination_airport=row[4],
                    price_economy=row[5],
                    price_business=row[6],
                    origin_city=row[8],
                    origin_country=row[9],
                    destination_city=row[10],
                    destination_country=row[11],
                    flight_duration=row[7]
                )
            flights.append(flight)
        
        return flights


class SmallFlight(Flight):
    """Represents a flight with a small plane"""
    
    def get_plane_size(self):
        return 'Small'
    
    def get_max_capacity(self):
        """Returns maximum capacity for small planes"""
        return len(self.get_seats())


class LargeFlight(Flight):
    """Represents a flight with a large plane - always has business class"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure large flights always have business class pricing
        if self.price_business is None:
            # Set default business price if not set (typically 2x economy)
            self.price_business = self.price_economy * 2
    
    def get_plane_size(self):
        return 'Large'
    
    def get_max_capacity(self):
        """Returns maximum capacity for large planes"""
        return len(self.get_seats())
    
    def has_business_class(self):
        """Large flights always have business class"""
        return True


# Order class moved to order.py
# Note: Import Order from order.py when needed to avoid circular import


# Helper functions for backward compatibility
def get_active_flights(origin=None, destination=None, date=None):
    """Backward compatibility wrapper"""
    flights = Flight.get_active_flights(origin, destination, date)
    # Convert to tuple format for existing templates
    result = []
    for flight in flights:
        result.append((
            flight.flight_id,
            flight.departure_time,
            flight.departure_date,
            flight.origin_airport,
            flight.destination_airport,
            flight.price_economy,
            flight.price_business,
            flight.flight_duration,
            flight.origin_city,
            flight.origin_country,
            flight.destination_city,
            flight.destination_country,
            flight.plane_id,
            flight.get_available_seats_count(),
            flight.get_destination_image()
        ))
    return result

def get_all_airports():
    """Returns list of all airports"""
    query = "SELECT airport_name, city, country FROM Airports ORDER BY city"
    return data.sql_query(query)

def get_destination_image(destination_code):
    """Backward compatibility wrapper"""
    destination_images = {
        'TLV': 'https://www.atarim.gov.il/wp-content/uploads/2020/06/Screenshot_1.png',
        'JFK': 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?auto=format&fit=crop&q=80&w=800',
        'LHR': 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&q=80&w=800',
        'CDG': 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&q=80&w=800',
        'NRT': 'https://www.elal.com/magazine/wp-content/uploads/2019/11/shutterstock_1030169917.jpg',
        'HND': 'https://www.elal.com/magazine/wp-content/uploads/2019/11/shutterstock_1030169917.jpg',
    }
    default_image = 'https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&q=80&w=800'
    return destination_images.get(destination_code, default_image)

def get_flight_details(flight_id):
    """Backward compatibility wrapper - returns tuple format"""
    flight = Flight.get_flight_by_id(flight_id)
    if not flight:
        return None
    return (
        flight.flight_id,
        flight.departure_time,
        flight.departure_date,
        flight.origin_airport,
        flight.destination_airport,
        flight.price_economy,
        flight.price_business,
        flight.plane_id,
        flight.origin_city,
        flight.origin_country,
        flight.destination_city,
        flight.destination_country
    )

def organize_seats_by_row(plane_id, flight_id):
    """Backward compatibility wrapper"""
    flight = Flight.get_flight_by_id(flight_id)
    if not flight:
        return {}
    return flight.organize_seats_by_row()

def process_seat_booking(user_email, flight_id, selected_seats):
    """Backward compatibility wrapper"""
    flight = Flight.get_flight_by_id(flight_id)
    if not flight:
        return None, "Flight not found"
    
    order = Order(email=user_email)
    return order.process_booking(flight, selected_seats)


# ==================== Flight Management Functions ====================

def is_long_flight(flight_duration_minutes):
    """
    Determines if a flight is considered 'long' based on duration.
    Flights over 6 hours (360 minutes) require long flight certification.
    """
    return flight_duration_minutes > 360


def get_crew_requirements(plane_size, is_long):
    """
    Determines crew requirements based on plane size and flight duration.
    
    Args:
        plane_size: 'Small' or 'Large'
        is_long: Boolean indicating if flight is long duration
    
    Returns:
        dict with 'pilots' and 'attendants' counts
    """
    if plane_size == 'Small':
        return {'pilots': 2, 'attendants': 3}
    else:  # Large
        return {'pilots': 3, 'attendants': 6}


def get_last_flight_destination_country(entity_id, entity_type):
    """
    Gets the destination country of the last flight for a plane, pilot, or attendant.
    
    Args:
        entity_id: plane_id, pilot_id, or attendant_id
        entity_type: 'plane', 'pilot', or 'attendant'
    
    Returns:
        country name or None if no previous flights
    """
    if entity_type == 'plane':
        query = """
            SELECT ad.country
            FROM Flights f
            JOIN Airports ad ON f.destination_airport_name = ad.airport_name
            WHERE f.plane_id = %s AND f.status != 'Cancelled'
            ORDER BY f.departure_date DESC, f.departure_time DESC
            LIMIT 1
        """
    elif entity_type == 'pilot':
        query = """
            SELECT ad.country
            FROM Pilots_In_Flights pif
            JOIN Flights f ON pif.flight_id = f.flight_id
            JOIN Airports ad ON f.destination_airport_name = ad.airport_name
            WHERE pif.pilot_id = %s AND f.status != 'Cancelled'
            ORDER BY f.departure_date DESC, f.departure_time DESC
            LIMIT 1
        """
    elif entity_type == 'attendant':
        query = """
            SELECT ad.country
            FROM Attendants_In_Flights aif
            JOIN Flights f ON aif.flight_id = f.flight_id
            JOIN Airports ad ON f.destination_airport_name = ad.airport_name
            WHERE aif.attendant_id = %s AND f.status != 'Cancelled'
            ORDER BY f.departure_date DESC, f.departure_time DESC
            LIMIT 1
        """
    else:
        return None
    
    result = data.sql_query(query, entity_id)
    if result and len(result) > 0:
        return result[0][0]
    return None


def get_available_planes(origin_country, is_long_flight=False, departure_date=None, departure_time=None):
    """
    Gets available planes that can be used for a flight from origin_country.
    A plane is available if its last flight destination country matches origin_country,
    or if it has no previous flights.
    Also checks that plane is not already assigned to another flight at the same time.
    
    For long flights (>6 hours), only Large planes are available.
    For short flights (<=6 hours), both Small and Large planes are available.
    
    All filtering is done in SQL for efficiency.
    
    Args:
        origin_country: Country of origin airport
        is_long_flight: Boolean indicating if flight is long duration (>6 hours)
        departure_date: Optional departure date to check for conflicts
        departure_time: Optional departure time to check for conflicts
    
    Returns:
        List of tuples (plane_id, manufacturer, size, purchase_date)
    """
    query = """
        SELECT DISTINCT p.plane_id, p.manufacturer, p.size, p.purchase_date
        FROM Planes p
        LEFT JOIN (
            SELECT f1.plane_id, f1.destination_airport_name, f1.departure_date, f1.departure_time,
                   ROW_NUMBER() OVER (PARTITION BY f1.plane_id ORDER BY f1.departure_date DESC, f1.departure_time DESC) as rn
            FROM Flights f1
            WHERE f1.status != 'Cancelled'
        ) last_flight ON p.plane_id = last_flight.plane_id AND last_flight.rn = 1
        LEFT JOIN Airports ad ON last_flight.destination_airport_name = ad.airport_name
        WHERE (
            -- Filter by size: long flights require Large planes only
            (%s = 0 OR p.size = 'Large')
            AND (
                -- Plane has no flights at all (last_flight.plane_id IS NULL)
                last_flight.plane_id IS NULL
                OR
                -- Plane's last flight destination matches origin country
                ad.country = %s
            )
    """
    
    params = []
    is_long = 1 if is_long_flight else 0
    params.append(is_long)
    params.append(origin_country)
    
    # Add check for time conflicts if date/time provided
    if departure_date and departure_time:
        query += """
            AND p.plane_id NOT IN (
                SELECT DISTINCT f2.plane_id
                FROM Flights f2
                WHERE f2.status != 'Cancelled'
                AND f2.departure_date = %s
                AND f2.departure_time = %s
            )
        """
        params.append(departure_date)
        params.append(departure_time)
    
    query += """
        )
        ORDER BY p.plane_id
    """
    
    return data.sql_query(query, *params)


def get_available_pilots(origin_country, origin_airport=None, is_long_flight=False, departure_date=None, departure_time=None):
    """
    Gets available pilots for a flight.
    A pilot is available if:
    1. Has long_flight_certified=True if flight is long
    2. Last flight destination matches origin_airport (or origin_country if airport not specified)
    3. Last flight arrival time is before new flight departure time
    4. Not assigned to another flight at the same time (if departure_date/time provided)
    
    All filtering is done in SQL for efficiency.
    
    Args:
        origin_country: Country of origin airport
        origin_airport: Optional origin airport name (for exact matching)
        is_long_flight: Whether flight requires long flight certification
        departure_date: Optional departure date to check for conflicts
        departure_time: Optional departure time to check for conflicts
    
    Returns:
        List of tuples (pilot_id, first_name_he, last_name_he, long_flight_certified)
    """
    # Base query for pilots matching certification and last flight destination
    query = """
        SELECT DISTINCT p.pilot_id, p.first_name_he, p.last_name_he, p.long_flight_certified
        FROM Pilots p
        LEFT JOIN (
            SELECT pif1.pilot_id, 
                   f1.destination_airport_name, 
                   f1.departure_date, 
                   f1.departure_time,
                   f1.flight_id,
                   fr1.flight_duration,
                   DATE_ADD(
                       DATE_ADD(f1.departure_date, INTERVAL TIME_TO_SEC(f1.departure_time) SECOND),
                       INTERVAL fr1.flight_duration MINUTE
                   ) as arrival_datetime,
                   ROW_NUMBER() OVER (PARTITION BY pif1.pilot_id ORDER BY f1.departure_date DESC, f1.departure_time DESC) as rn
            FROM Pilots_In_Flights pif1
            JOIN Flights f1 ON pif1.flight_id = f1.flight_id
            JOIN FlightRoutes fr1 ON f1.origin_airport_name = fr1.origin_airport_name 
                                  AND f1.destination_airport_name = fr1.destination_airport_name
            WHERE f1.status != 'Cancelled'
        ) last_flight ON p.pilot_id = last_flight.pilot_id AND last_flight.rn = 1
        LEFT JOIN Airports ad ON last_flight.destination_airport_name = ad.airport_name
        WHERE p.long_flight_certified >= %s
        AND (
            -- Pilot has no flights at all (last_flight.pilot_id IS NULL)
            last_flight.pilot_id IS NULL
            OR
            (
                -- Pilot's last flight destination matches origin airport (if specified) or origin country
                (%s IS NULL AND ad.country = %s)
                OR
                (%s IS NOT NULL AND last_flight.destination_airport_name = %s)
            )
    """
    
    params = []
    is_long = 1 if is_long_flight else 0
    params.append(is_long)
    params.append(origin_airport)  # For NULL check
    params.append(origin_country)  # For country match
    params.append(origin_airport)  # For airport check
    params.append(origin_airport)  # For airport match
    
    # Add check for arrival time before departure time if date/time provided
    if departure_date and departure_time:
        query += """
            AND (
                -- No previous flight OR arrival time is before new departure time
                last_flight.arrival_datetime IS NULL
                OR
                last_flight.arrival_datetime < DATE_ADD(
                    DATE_ADD(%s, INTERVAL TIME_TO_SEC(%s) SECOND),
                    INTERVAL 0 MINUTE
                )
            )
        """
        params.append(departure_date)
        params.append(departure_time)
    
    # Add check for time conflicts (same departure time) if date/time provided
    if departure_date and departure_time:
        query += """
        AND p.pilot_id NOT IN (
            SELECT DISTINCT pif2.pilot_id
            FROM Pilots_In_Flights pif2
            JOIN Flights f2 ON pif2.flight_id = f2.flight_id
            WHERE f2.status != 'Cancelled'
            AND f2.departure_date = %s
            AND f2.departure_time = %s
        )
        """
        params.append(departure_date)
        params.append(departure_time)
    
    query += """
        )
    """
    
    query += " ORDER BY p.pilot_id"
    
    return data.sql_query(query, *params)


def get_available_attendants(origin_country, origin_airport=None, is_long_flight=False, departure_date=None, departure_time=None):
    """
    Gets available attendants for a flight.
    An attendant is available if:
    1. Has long_flight_certified=True if flight is long
    2. Last flight destination matches origin_airport (or origin_country if airport not specified)
    3. Last flight arrival time is before new flight departure time
    4. Not assigned to another flight at the same time (if departure_date/time provided)
    
    All filtering is done in SQL for efficiency.
    
    Args:
        origin_country: Country of origin airport
        origin_airport: Optional origin airport name (for exact matching)
        is_long_flight: Whether flight requires long flight certification
        departure_date: Optional departure date to check for conflicts
        departure_time: Optional departure time to check for conflicts
    
    Returns:
        List of tuples (attendant_id, first_name_he, last_name_he, long_flight_certified)
    """
    # Base query for attendants matching certification and last flight destination
    query = """
        SELECT DISTINCT a.attendant_id, a.first_name_he, a.last_name_he, a.long_flight_certified
        FROM Attendants a
        LEFT JOIN (
            SELECT aif1.attendant_id, 
                   f1.destination_airport_name, 
                   f1.departure_date, 
                   f1.departure_time,
                   f1.flight_id,
                   fr1.flight_duration,
                   DATE_ADD(
                       DATE_ADD(f1.departure_date, INTERVAL TIME_TO_SEC(f1.departure_time) SECOND),
                       INTERVAL fr1.flight_duration MINUTE
                   ) as arrival_datetime,
                   ROW_NUMBER() OVER (PARTITION BY aif1.attendant_id ORDER BY f1.departure_date DESC, f1.departure_time DESC) as rn
            FROM Attendants_In_Flights aif1
            JOIN Flights f1 ON aif1.flight_id = f1.flight_id
            JOIN FlightRoutes fr1 ON f1.origin_airport_name = fr1.origin_airport_name 
                                  AND f1.destination_airport_name = fr1.destination_airport_name
            WHERE f1.status != 'Cancelled'
        ) last_flight ON a.attendant_id = last_flight.attendant_id AND last_flight.rn = 1
        LEFT JOIN Airports ad ON last_flight.destination_airport_name = ad.airport_name
        WHERE a.long_flight_certified >= %s
        AND (
            -- Attendant has no flights at all (last_flight.attendant_id IS NULL)
            last_flight.attendant_id IS NULL
            OR
            (
                -- Attendant's last flight destination matches origin airport (if specified) or origin country
                (%s IS NULL AND ad.country = %s)
                OR
                (%s IS NOT NULL AND last_flight.destination_airport_name = %s)
            )
    """
    
    params = []
    is_long = 1 if is_long_flight else 0
    params.append(is_long)
    params.append(origin_airport)  # For NULL check
    params.append(origin_country)  # For country match
    params.append(origin_airport)  # For airport check
    params.append(origin_airport)  # For airport match
    
    # Add check for arrival time before departure time if date/time provided
    if departure_date and departure_time:
        query += """
            AND (
                -- No previous flight OR arrival time is before new departure time
                last_flight.arrival_datetime IS NULL
                OR
                last_flight.arrival_datetime < DATE_ADD(
                    DATE_ADD(%s, INTERVAL TIME_TO_SEC(%s) SECOND),
                    INTERVAL 0 MINUTE
                )
            )
        """
        params.append(departure_date)
        params.append(departure_time)
    
    # Add check for time conflicts (same departure time) if date/time provided
    if departure_date and departure_time:
        query += """
        AND a.attendant_id NOT IN (
            SELECT DISTINCT aif2.attendant_id
            FROM Attendants_In_Flights aif2
            JOIN Flights f2 ON aif2.flight_id = f2.flight_id
            WHERE f2.status != 'Cancelled'
            AND f2.departure_date = %s
            AND f2.departure_time = %s
        )
        """
        params.append(departure_date)
        params.append(departure_time)
    
    query += """
        )
    """
    
    query += " ORDER BY a.attendant_id"
    
    return data.sql_query(query, *params)


def get_flight_route_info(origin_airport, destination_airport):
    """
    Gets flight route information including duration.
    
    Returns:
        tuple (flight_duration, origin_country, destination_country) or None
    """
    query = """
        SELECT fr.flight_duration, ao.country, ad.country
        FROM FlightRoutes fr
        JOIN Airports ao ON fr.origin_airport_name = ao.airport_name
        JOIN Airports ad ON fr.destination_airport_name = ad.airport_name
        WHERE fr.origin_airport_name = %s AND fr.destination_airport_name = %s
    """
    result = data.sql_query(query, origin_airport, destination_airport)
    if result and len(result) > 0:
        return result[0]
    return None


def get_next_flight_id():
    """Gets the next available flight_id"""
    query = "SELECT MAX(flight_id) FROM Flights"
    result = data.sql_query(query)
    if result and result[0][0] is not None:
        return result[0][0] + 1
    return 1001  # Starting flight ID


def add_flight(departure_date, departure_time, origin_airport, destination_airport,
                plane_id, pilot_ids, attendant_ids, price_economy, price_business=None):
    """
    Adds a new flight to the database.
    Note: All validations are done in SQL queries (get_available_planes, get_available_pilots, etc.)
    so we only need basic checks here.
    
    Args:
        departure_date: Date string (YYYY-MM-DD)
        departure_time: Time string (HH:MM:SS)
        origin_airport: Origin airport code
        destination_airport: Destination airport code
        plane_id: Plane ID
        pilot_ids: List of pilot IDs
        attendant_ids: List of attendant IDs
        price_economy: Economy class price
        price_business: Business class price (optional, required for large planes)
    
    Returns:
        tuple (success: bool, flight_id: int or None, error_message: str or None)
    """
    try:
        # 1. Validate route exists
        route_info = get_flight_route_info(origin_airport, destination_airport)
        if not route_info:
            return False, None, "Route does not exist in database"
        
        flight_duration, origin_country, destination_country = route_info
        
        # 2. Get plane size (needed for crew requirements and business class check)
        plane_query = "SELECT size FROM Planes WHERE plane_id = %s"
        plane_result = data.sql_query(plane_query, plane_id)
        if not plane_result:
            return False, None, "Plane not found"
        
        plane_size = plane_result[0][0]
        is_long = is_long_flight(flight_duration)
        crew_reqs = get_crew_requirements(plane_size, is_long)
        
        # 3. Basic validation - check counts match requirements
        if len(pilot_ids) != crew_reqs['pilots']:
            return False, None, f"Need exactly {crew_reqs['pilots']} pilots for {plane_size} plane"
        
        if len(attendant_ids) != crew_reqs['attendants']:
            return False, None, f"Need exactly {crew_reqs['attendants']} attendants for {plane_size} plane"
        
        # 4. Validate business class price for large planes
        if plane_size == 'Large' and price_business is None:
            return False, None, "Business class price is required for large planes"
        
        # 5. Get next flight ID
        flight_id = get_next_flight_id()
        
        # 6. Insert flight
        flight_insert = """
            INSERT INTO Flights (flight_id, departure_time, departure_date, status, 
                                plane_id, origin_airport_name, destination_airport_name,
                                price_economy, price_business)
            VALUES (%s, %s, %s, 'Active', %s, %s, %s, %s, %s)
        """
        data.sql_insert(flight_insert, flight_id, departure_time, departure_date, 
                       plane_id, origin_airport, destination_airport,
                       price_economy, price_business)
        
        # 7. Assign pilots
        for pilot_id in pilot_ids:
            pilot_insert = "INSERT INTO Pilots_In_Flights (pilot_id, flight_id) VALUES (%s, %s)"
            data.sql_insert(pilot_insert, pilot_id, flight_id)
        
        # 8. Assign attendants
        for attendant_id in attendant_ids:
            attendant_insert = "INSERT INTO Attendants_In_Flights (attendant_id, flight_id) VALUES (%s, %s)"
            data.sql_insert(attendant_insert, attendant_id, flight_id)
        
        return True, flight_id, None
        
    except Exception as e:
        return False, None, f"Error adding flight: {str(e)}"
