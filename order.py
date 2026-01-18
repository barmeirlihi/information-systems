"""
Order class - represents an order in the Orders table
Contains only fields that are saved to the database: order_id, email, order_status, order_date, total_payment
Also handles booking workflow (flight, seats) for session management
"""
from datetime import date
import data
from flights import Flight


class Order:
    """Represents an order with fields matching the Orders table in database"""
    
    _next_order_id = None
    
    def __init__(self, order_id=None, email=None, order_status='Active', 
                 order_date=None, total_payment=0.0):
        """
        Initialize an Order object with fields from Orders table
        
        Args:
            order_id: Order ID (primary key)
            email: User email (foreign key to Users)
            order_status: Order status (default: 'Confirmed')
            order_date: Order date (default: today)
            total_payment: Total payment amount
        """
        self.order_id = order_id
        self.email = email
        self.order_status = order_status
        self.order_date = order_date if order_date else date.today()
        self.total_payment = float(total_payment)
        
        # Additional fields for booking workflow (not saved to DB, used for session)
        self.flight_id = None
        self.flight = None
        self.selected_seats = []
        self.seat_details = []
        self.user_data = {}
    
    @staticmethod
    def get_next_order_id():
        """Gets the next available order ID"""
        if Order._next_order_id is None:
            query = "SELECT MAX(order_id) FROM Orders"
            result = data.sql_query(query)
            if result and result[0][0]:
                Order._next_order_id = result[0][0] + 1
            else:
                Order._next_order_id = 501  # Starting order_id if table is empty
        else:
            Order._next_order_id += 1
        return Order._next_order_id
    
    def create(self):
        """
        Creates the order in the database
        Saves only fields from Orders table: order_id, email, order_status, order_date, total_payment
        
        Returns:
            order_id
        """
        if self.order_id is None:
            self.order_id = Order.get_next_order_id()
        
        query = """
            INSERT INTO Orders (order_id, email, order_status, order_date, total_payment)
            VALUES (%s, %s, %s, %s, %s)
        """
        data.sql_insert(query, self.order_id, self.email, self.order_status, 
                       self.order_date, self.total_payment)
        return self.order_id
    
    def process_booking(self, flight, selected_seats):
        """
        Processes a complete seat booking
        Validates seats, creates order in DB, and books seats
        
        Args:
            flight: Flight object
            selected_seats: List of selected seat strings
            
        Returns:
            (order_id, error_message)
        """
        # Validate seat selection
        total_price, seat_details, error = flight.validate_seat_selection(selected_seats)
        
        if error:
            return None, error
        
        # Set order details (fields that go to DB)
        self.total_payment = total_price
        # Note: self.email should be set before calling this method
        
        if not self.email:
            return None, "Email is required for order creation"
        
        # Create order in database
        order_id = self.create()
        
        # Book all selected seats
        flight.book_seats(order_id, seat_details)
        
        return order_id, None
    
    def save_to_session(self, session):
        """Saves order data to Flask session (including booking workflow data)"""
        session['booking'] = {
            'flight_id': self.flight_id,
            'selected_seats': self.selected_seats,
            'total_payment': self.total_payment,
            'seat_details': self.seat_details,
            'user_data': self.user_data
        }
    
    @classmethod
    def from_session(cls, session, flight_id):
        """
        Creates an Order object from session data
        
        Returns:
            Order object or None if not found in session
        """
        booking_data = session.get('booking')
        if not booking_data or booking_data.get('flight_id') != flight_id:
            return None
        
        # Get flight object
        flight = Flight.get_flight_by_id(flight_id)
        if not flight:
            return None
        
        # Create Order object
        # Handle both 'total_payment' and 'total_price' keys for compatibility
        total_payment = booking_data.get('total_payment') or booking_data.get('total_price', 0.0)
        order = cls(
            email=session.get('user_email'),
            total_payment=total_payment
        )
        
        # Set booking workflow fields (not in DB)
        order.flight_id = flight_id
        order.flight = flight
        order.selected_seats = booking_data['selected_seats']
        order.seat_details = booking_data['seat_details']
        order.user_data = booking_data.get('user_data', {})
        
        return order
    
    @classmethod
    def create_from_seat_selection(cls, flight, selected_seats, user_email):
        """
        Factory method to create Order from seat selection
        
        Args:
            flight: Flight object
            selected_seats: List of selected seat strings
            user_email: Email of the user
            
        Returns:
            (Order object, error_message)
        """
        # Validate seat selection
        total_price, seat_details, error = flight.validate_seat_selection(selected_seats)
        
        if error:
            return None, error
        
        # Create Order object
        order = cls(
            email=user_email,
            total_payment=total_price
        )
        
        # Set booking workflow fields (not in DB)
        order.flight_id = flight.flight_id
        order.flight = flight
        order.selected_seats = selected_seats
        order.seat_details = seat_details
        
        return order, None
    
    def get_confirmation_data(self):
        """
        Returns data needed for confirmation page
        
        Returns:
            Dictionary with confirmation data
        """
        return {
            'flight': self.flight,
            'booking': {
                'selected_seats': self.selected_seats,
                'total_price': self.total_payment,  # For backward compatibility
                'total_payment': self.total_payment,  # Main key
                'seat_details': self.seat_details
            },
            'user_data': self.user_data,
            'order_id': self.order_id
        }
    
    def to_dict(self):
        """Converts order to dictionary for session storage and template rendering"""
        return {
            'flight_id': self.flight_id,
            'selected_seats': self.selected_seats,
            'total_price': self.total_payment,  # Use total_price for template consistency
            'total_payment': self.total_payment,  # Keep both for compatibility
            'seat_details': self.seat_details,
            'user_data': self.user_data
        }
    
    @classmethod
    def get_by_id(cls, order_id):
        """
        Gets an order by order_id from database
        
        Args:
            order_id: Order ID
            
        Returns:
            Order object or None if not found
        """
        query = """
            SELECT order_id, email, order_status, order_date, total_payment
            FROM Orders
            WHERE order_id = %s
        """
        result = data.sql_query(query, order_id)
        if not result:
            return None
        
        row = result[0]
        order = cls(
            order_id=row[0],
            email=row[1],
            order_status=row[2],
            order_date=row[3],
            total_payment=row[4]
        )
        
        # Get flight info for this order
        order.load_flight_info()
        
        return order
    
    @classmethod
    def get_by_email(cls, email):
        """
        Gets all orders for a given email from database
        
        Args:
            email: User email
            
        Returns:
            List of Order objects
        """
        query = """
            SELECT order_id, email, order_status, order_date, total_payment
            FROM Orders
            WHERE email = %s
            ORDER BY order_date DESC, order_id DESC
        """
        result = data.sql_query(query, email)
        orders = []
        
        for row in result:
            order = cls(
                order_id=row[0],
                email=row[1],
                order_status=row[2],
                order_date=row[3],
                total_payment=row[4]
            )
            # Get flight info for this order
            order.load_flight_info()
            orders.append(order)
        
        return orders
    
    def load_flight_info(self):
        """Loads flight information for this order from FlightTickets table"""
        query = """
            SELECT DISTINCT flight_id
            FROM FlightTickets
            WHERE order_id = %s
            LIMIT 1
        """
        result = data.sql_query(query, self.order_id)
        if result:
            flight_id = result[0][0]
            self.flight_id = flight_id
            # Get flight object (include all statuses to get cancelled flights too)
            self.flight = Flight.get_flight_by_id(flight_id, include_all_statuses=True)
            
            # If flight not found, try to get it directly from database
            if not self.flight:
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
                result = data.sql_query(query, flight_id)
                if result:
                    row = result[0]
                    plane_size = row[13]
                    
                    # Get flight duration
                    duration_query = """
                        SELECT flight_duration
                        FROM FlightRoutes
                        WHERE origin_airport_name = %s AND destination_airport_name = %s
                    """
                    duration_result = data.sql_query(duration_query, row[5], row[6])
                    flight_duration = duration_result[0][0] if duration_result else None
                    
                    if plane_size == 'Small':
                        from flights import SmallFlight
                        self.flight = SmallFlight(
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
                    else:
                        from flights import LargeFlight
                        self.flight = LargeFlight(
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
            
            # Get seat details
            seat_query = """
                SELECT seat_row, seat_column
                FROM FlightTickets
                WHERE order_id = %s AND flight_id = %s
                ORDER BY seat_row, seat_column
            """
            seat_result = data.sql_query(seat_query, self.order_id, flight_id)
            self.seat_details = [(row[0], row[1]) for row in seat_result]
            self.selected_seats = [f"{row[0]}-{row[1]}" for row in seat_result]
    
    def get_display_status(self):
        """
        Determines the display status based on order status and flight status
        Returns: (status_text, cancellation_fee, final_price)
        """
        from datetime import date, datetime, timedelta
        
        # If order was cancelled by customer
        if self.order_status == 'Cancelled' or self.order_status == 'Cancelled by Customer':
            cancellation_fee = self.total_payment * 0.05
            return ('Cancelled', cancellation_fee, cancellation_fee)
        
        # If order was cancelled by system
        if self.order_status == 'Cancelled by System':
            return ('Cancelled by System', 0.0, 0.0)
        
        # If flight doesn't exist or was cancelled
        if not self.flight:
            if self.order_status == 'Cancelled by System':
                return ('Cancelled by System', 0.0, 0.0)
            return ('Not Available', 0.0, self.total_payment)
        
        # Check if flight occurred (departure date passed)
        flight_date = self.flight.departure_date
        flight_time = self.flight.departure_time
        
        if isinstance(flight_date, str):
            try:
                flight_date = datetime.strptime(flight_date, '%Y-%m-%d').date()
            except:
                # Try other date formats if needed
                pass
        
        # Combine date and time for accurate comparison
        from datetime import time as dt_time, timedelta
        if isinstance(flight_date, date) and flight_time:
            flight_time_obj = None
            
            if isinstance(flight_time, str):
                try:
                    time_parts = flight_time.split(':')
                    hour = int(time_parts[0])
                    minute = int(time_parts[1]) if len(time_parts) > 1 else 0
                    flight_time_obj = dt_time(hour=hour, minute=minute)
                except:
                    flight_time_obj = dt_time(0, 0)
            elif isinstance(flight_time, timedelta):
                # Handle timedelta from mysql.connector
                total_seconds = int(flight_time.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                flight_time_obj = dt_time(hour=hours, minute=minutes)
            elif isinstance(flight_time, dt_time):
                flight_time_obj = flight_time
            else:
                flight_time_obj = dt_time(0, 0)
            
            if flight_time_obj:
                flight_datetime = datetime.combine(flight_date, flight_time_obj)
                if flight_datetime < datetime.now():
                    return ('Completed', 0.0, self.total_payment)
        
        # Check if flight was cancelled by system
        if self.flight.status == 'Cancelled' or self.order_status == 'Cancelled by System':
            return ('Cancelled by System', 0.0, 0.0)
        
        # Active order
        if self.order_status in ['Confirmed', 'Active']:
            return ('Active', 0.0, self.total_payment)
        
        # Default to active if status is unknown
        return ('Active', 0.0, self.total_payment)
    
    def cancel_by_customer(self):
        """
        Cancels order by customer - updates status to 'Cancelled by Customer'
        Can only be cancelled if at least 36 hours before departure
        
        Returns:
            (success, error_message)
        """
        from datetime import datetime, timedelta
        
        # Check if order can be cancelled
        status, _, _ = self.get_display_status()
        if status != 'Active':
            return False, "Order cannot be cancelled"
        
        # Check if flight exists
        if not self.flight:
            return False, "Flight information not available"
        
        # Check if cancellation is allowed (at least 36 hours before departure)
        flight_date = self.flight.departure_date
        flight_time = self.flight.departure_time
        
        if isinstance(flight_date, str):
            try:
                flight_date = datetime.strptime(flight_date, '%Y-%m-%d').date()
            except:
                return False, "Invalid flight date format"
        
        # Combine date and time
        from datetime import time as dt_time, timedelta
        flight_time_obj = None
        
        if isinstance(flight_time, str):
            try:
                time_parts = flight_time.split(':')
                hour = int(time_parts[0])
                minute = int(time_parts[1]) if len(time_parts) > 1 else 0
                flight_time_obj = dt_time(hour=hour, minute=minute)
            except:
                flight_time_obj = dt_time(0, 0)
        elif isinstance(flight_time, timedelta):
            # Handle timedelta from mysql.connector
            total_seconds = int(flight_time.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            flight_time_obj = dt_time(hour=hours, minute=minutes)
        elif isinstance(flight_time, dt_time):
            flight_time_obj = flight_time
        else:
            flight_time_obj = dt_time(0, 0)
        
        if flight_time_obj:
            flight_datetime = datetime.combine(flight_date, flight_time_obj)
        
        # Check if at least 36 hours before departure
        time_until_departure = flight_datetime - datetime.now()
        if time_until_departure < timedelta(hours=36):
            return False, "Order can only be cancelled at least 36 hours before departure"
        
        # Update order status
        query = """
            UPDATE Orders
            SET order_status = 'Cancelled'
            WHERE order_id = %s
        """
        try:
            data.sql_insert(query, self.order_id)
            self.order_status = 'Cancelled'
            
            # Cancel flight tickets (free up seats)
            if self.flight:
                self.flight.cancel_order_seats(self.order_id)
            
            return True, None
        except Exception as e:
            return False, f"Error cancelling order: {str(e)}"
    
    def get_cancellation_fee(self):
        """Returns the cancellation fee (5% of total payment)"""
        return self.total_payment * 0.05

