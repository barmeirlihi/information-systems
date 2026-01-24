"""
Script to populate the FlyTau database with extensive data
- Adds 10 airports (total)
- Creates routes from every airport to every other airport (90 routes)
- Adds many flights with different statuses
- Adds orders and tickets
"""

import data
from datetime import datetime, timedelta, date
import random

def add_airports():
    """Add 6 more airports to reach 10 total"""
    airports = [
        ('DXB', 'UAE', 'Dubai'),
        ('FRA', 'Germany', 'Frankfurt'),
        ('IST', 'Turkey', 'Istanbul'),
        ('MAD', 'Spain', 'Madrid'),
        ('AMS', 'Netherlands', 'Amsterdam'),
        ('BCN', 'Spain', 'Barcelona'),
    ]
    
    for airport_code, country, city in airports:
        try:
            query = "INSERT INTO Airports (airport_name, country, city) VALUES (%s, %s, %s)"
            data.sql_insert(query, airport_code, country, city)
            print(f"Added airport: {airport_code} - {city}, {country}")
        except Exception as e:
            print(f"Airport {airport_code} might already exist: {e}")

def add_routes():
    """Create routes from every airport to every other airport"""
    # Get all airports
    query = "SELECT airport_name FROM Airports ORDER BY airport_name"
    result = data.sql_query(query)
    airports = [row[0] for row in result]
    
    print(f"\nFound {len(airports)} airports: {airports}")
    
    # Duration ranges (in minutes) based on typical flight times
    # Short flights: 180-360 minutes (3-6 hours)
    # Long flights: 420-720 minutes (7-12 hours)
    duration_ranges = {
        # Within Europe
        'EUROPE_SHORT': (180, 300),
        # Europe to Middle East
        'EUROPE_MIDDLE_EAST': (240, 360),
        # Europe/US to Middle East
        'LONG_EAST': (420, 600),
        # Transatlantic
        'TRANSATLANTIC': (600, 720),
        # Very long (e.g., US to Middle East)
        'VERY_LONG': (660, 840),
    }
    
    def get_duration(origin, destination):
        """Calculate flight duration based on route"""
        # Define airport regions
        europe = ['CDG', 'LHR', 'FRA', 'MAD', 'AMS', 'BCN']
        middle_east = ['TLV', 'DXB', 'IST']
        usa = ['JFK']
        
        origin_region = None
        dest_region = None
        
        if origin in europe:
            origin_region = 'EUROPE'
        elif origin in middle_east:
            origin_region = 'MIDDLE_EAST'
        elif origin in usa:
            origin_region = 'USA'
            
        if destination in europe:
            dest_region = 'EUROPE'
        elif destination in middle_east:
            dest_region = 'MIDDLE_EAST'
        elif destination in usa:
            dest_region = 'USA'
        
        # Calculate duration
        if origin_region == dest_region:
            if origin_region == 'EUROPE':
                return random.randint(180, 300)  # 3-5 hours
            else:
                return random.randint(240, 360)  # 4-6 hours
        elif (origin_region == 'EUROPE' and dest_region == 'MIDDLE_EAST') or \
             (origin_region == 'MIDDLE_EAST' and dest_region == 'EUROPE'):
            return random.randint(240, 360)  # 4-6 hours
        elif (origin_region == 'USA' and dest_region == 'MIDDLE_EAST') or \
             (origin_region == 'MIDDLE_EAST' and dest_region == 'USA'):
            return random.randint(660, 840)  # 11-14 hours
        elif (origin_region == 'USA' and dest_region == 'EUROPE') or \
             (origin_region == 'EUROPE' and dest_region == 'USA'):
            return random.randint(600, 720)  # 10-12 hours
        else:
            return random.randint(300, 480)  # Default 5-8 hours
    
    routes_added = 0
    for origin in airports:
        for destination in airports:
            if origin != destination:
                duration = get_duration(origin, destination)
                try:
                    query = """
                        INSERT INTO FlightRoutes (origin_airport_name, destination_airport_name, flight_duration)
                        VALUES (%s, %s, %s)
                    """
                    data.sql_insert(query, origin, destination, duration)
                    routes_added += 1
                    if routes_added % 10 == 0:
                        print(f"Added {routes_added} routes...")
                except Exception as e:
                    # Route might already exist
                    pass
    
    print(f"\nTotal routes added/updated: {routes_added}")

def add_flights():
    """Add many flights with different statuses and dates"""
    # Get all routes
    query = """
        SELECT origin_airport_name, destination_airport_name, flight_duration
        FROM FlightRoutes
        ORDER BY origin_airport_name, destination_airport_name
    """
    routes = data.sql_query(query)
    
    # Get all planes
    query = "SELECT plane_id, size FROM Planes ORDER BY plane_id"
    planes_result = data.sql_query(query)
    planes_list = [(row[0], row[1]) for row in planes_result]
    
    if not planes_list:
        print("No planes found in database!")
        return
    
    # Get pilots and attendants
    pilots_query = "SELECT pilot_id FROM Pilots ORDER BY pilot_id"
    pilots_result = data.sql_query(pilots_query)
    pilots_list = [row[0] for row in pilots_result]
    
    attendants_query = "SELECT attendant_id FROM Attendants ORDER BY attendant_id"
    attendants_result = data.sql_query(attendants_query)
    attendants_list = [row[0] for row in attendants_result]
    
    if not pilots_list or not attendants_list:
        print("No pilots or attendants found!")
        return
    
    # Statuses and their probabilities
    statuses = ['Active', 'Landed', 'Cancelled']
    
    # Generate flights for the past 6 months and next 6 months
    today = date.today()
    start_date = today - timedelta(days=180)
    end_date = today + timedelta(days=180)
    
    flight_id = 2000  # Start from 2000 to avoid conflicts
    flights_added = 0
    
    # Generate flights
    for route in routes:
        origin, destination, duration = route
        
        # Determine if this is a long flight (>6 hours = 360 minutes)
        is_long = duration > 360
        
        # Filter planes by size (long flights need large planes)
        available_planes = [p for p in planes_list if p[1] == 'Large'] if is_long else planes_list
        
        if not available_planes:
            continue
        
        # Generate 3-5 flights per route
        num_flights = random.randint(3, 5)
        
        for _ in range(num_flights):
            # Random date
            days_offset = random.randint(0, (end_date - start_date).days)
            flight_date = start_date + timedelta(days=days_offset)
            
            # Random time
            hour = random.randint(6, 23)
            minute = random.choice([0, 15, 30, 45])
            departure_time = f"{hour:02d}:{minute:02d}:00"
            
            # Determine status based on date
            if flight_date < today:
                status = random.choice(['Landed', 'Cancelled'])
            elif flight_date == today:
                status = random.choice(['Active', 'Cancelled'])
            else:
                status = random.choice(['Active', 'Cancelled'])
            
            # Select plane
            plane_id, plane_size = random.choice(available_planes)
            
            # Calculate prices
            base_price = random.randint(200, 800)
            price_economy = base_price
            price_business = base_price * 2 if plane_size == 'Large' else None
            
            try:
                # Insert flight
                flight_query = """
                    INSERT INTO Flights (flight_id, departure_time, departure_date, status, 
                                       plane_id, origin_airport_name, destination_airport_name,
                                       price_economy, price_business)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                data.sql_insert(flight_query, flight_id, departure_time, flight_date, status,
                               plane_id, origin, destination, price_economy, price_business)
                
                # Assign crew
                # Get crew requirements
                if plane_size == 'Small':
                    num_pilots = 2
                    num_attendants = 3
                else:
                    num_pilots = 3
                    num_attendants = 6
                
                # Filter crew by certification for long flights
                if is_long:
                    pilots_query_filtered = """
                        SELECT pilot_id FROM Pilots WHERE long_flight_certified = 1
                    """
                    available_pilots = [row[0] for row in data.sql_query(pilots_query_filtered)]
                    
                    attendants_query_filtered = """
                        SELECT attendant_id FROM Attendants WHERE long_flight_certified = 1
                    """
                    available_attendants = [row[0] for row in data.sql_query(attendants_query_filtered)]
                else:
                    available_pilots = pilots_list
                    available_attendants = attendants_list
                
                if len(available_pilots) >= num_pilots and len(available_attendants) >= num_attendants:
                    # Assign pilots
                    selected_pilots = random.sample(available_pilots, num_pilots)
                    for pilot_id in selected_pilots:
                        pilot_flight_query = "INSERT INTO Pilots_In_Flights (pilot_id, flight_id) VALUES (%s, %s)"
                        try:
                            data.sql_insert(pilot_flight_query, pilot_id, flight_id)
                        except:
                            pass
                    
                    # Assign attendants
                    selected_attendants = random.sample(available_attendants, num_attendants)
                    for attendant_id in selected_attendants:
                        attendant_flight_query = "INSERT INTO Attendants_In_Flights (attendant_id, flight_id) VALUES (%s, %s)"
                        try:
                            data.sql_insert(attendant_flight_query, attendant_id, flight_id)
                        except:
                            pass
                
                flight_id += 1
                flights_added += 1
                
                if flights_added % 50 == 0:
                    print(f"Added {flights_added} flights...")
                    
            except Exception as e:
                # Flight might already exist or constraint violation
                flight_id += 1
                continue
    
    print(f"\nTotal flights added: {flights_added}")

def add_orders_and_tickets():
    """Add orders and tickets for landed flights"""
    # Get landed flights
    query = """
        SELECT f.flight_id, f.plane_id, f.price_economy, f.price_business
        FROM Flights f
        WHERE f.status = 'Landed'
        ORDER BY f.departure_date DESC
        LIMIT 100
    """
    flights = data.sql_query(query)
    
    if not flights:
        print("No landed flights found for orders")
        return
    
    # Get users and guests
    users_query = "SELECT email FROM Users"
    users_result = data.sql_query(users_query)
    users_list = [row[0] for row in users_result]
    
    guests_query = "SELECT UserEmail FROM Guests"
    guests_result = data.sql_query(guests_query)
    guests_list = [row[0] for row in guests_result]
    
    all_emails = users_list + guests_list
    
    if not all_emails:
        print("No users or guests found")
        return
    
    # Get seats for planes
    order_id = 1000
    orders_added = 0
    
    for flight in flights[:50]:  # Limit to 50 flights
        flight_id, plane_id, price_economy, price_business = flight
        
        # Get available seats for this plane
        seats_query = """
            SELECT seat_row, seat_column, seat_class
            FROM Seats
            WHERE plane_id = %s
            ORDER BY seat_row, seat_column
        """
        seats = data.sql_query(seats_query, plane_id)
        
        if not seats:
            continue
        
        # Create 1-3 orders per flight
        num_orders = random.randint(1, 3)
        
        for _ in range(num_orders):
            # Select random email
            email = random.choice(all_emails)
            
            # Select 1-4 seats
            num_seats = random.randint(1, min(4, len(seats)))
            selected_seats = random.sample(seats, num_seats)
            
            # Calculate total price
            total_price = 0.0
            for seat_row, seat_column, seat_class in selected_seats:
                if seat_class == 'Business' and price_business:
                    total_price += float(price_business)
                else:
                    total_price += float(price_economy)
            
            # Random order date (before flight date)
            flight_date_query = "SELECT departure_date FROM Flights WHERE flight_id = %s"
            flight_date_result = data.sql_query(flight_date_query, flight_id)
            if not flight_date_result:
                continue
            
            flight_date = flight_date_result[0][0]
            if isinstance(flight_date, str):
                flight_date = datetime.strptime(flight_date, '%Y-%m-%d').date()
            
            order_date = flight_date - timedelta(days=random.randint(1, 60))
            
            # Random status
            order_status = random.choice(['Confirmed', 'Cancelled'])
            
            try:
                # Insert order
                order_query = """
                    INSERT INTO Orders (order_id, email, order_status, order_date, total_payment)
                    VALUES (%s, %s, %s, %s, %s)
                """
                data.sql_insert(order_query, order_id, email, order_status, order_date, total_price)
                
                # Insert tickets
                for seat_row, seat_column, seat_class in selected_seats:
                    ticket_query = """
                        INSERT INTO FlightTickets (order_id, flight_id, plane_id, seat_row, seat_column)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    try:
                        data.sql_insert(ticket_query, order_id, flight_id, plane_id, seat_row, seat_column)
                    except:
                        pass
                
                order_id += 1
                orders_added += 1
                
            except Exception as e:
                order_id += 1
                continue
    
    print(f"\nTotal orders added: {orders_added}")

def main():
    """Main function to populate database"""
    print("=" * 60)
    print("FlyTau Database Population Script")
    print("=" * 60)
    
    try:
        print("\n1. Adding airports...")
        add_airports()
        
        print("\n2. Adding routes (from every airport to every other airport)...")
        add_routes()
        
        print("\n3. Adding flights...")
        add_flights()
        
        print("\n4. Adding orders and tickets...")
        add_orders_and_tickets()
        
        print("\n" + "=" * 60)
        print("Database population completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

