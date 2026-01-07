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
        Also updates all related orders to 'Cancelled by System'
        
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
            
            # Update all orders for this flight to 'Cancelled by System'
            orders_query = """
                UPDATE Orders
                SET order_status = 'Cancelled by System'
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
            'JFK': 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?auto=format&fit=crop&q=80&w=800',
            'LHR': 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&q=80&w=800',
            'CDG': 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&q=80&w=800',
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
