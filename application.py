from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from datetime import timedelta, date
import os

import data
import guest
import users
from data import *
from users import *
from flights import *
from guest import *
from order import Order
import reports

session_dir = os.path.join(os.getcwd(), "flask_session_data")
try:
    if not os.path.exists(session_dir):
        os.makedirs(session_dir, exist_ok=True)
except (OSError, PermissionError) as e:
    # If we can't create the directory, use a fallback location
    session_dir = "/tmp/flask_session_data"
    try:
        os.makedirs(session_dir, exist_ok=True)
    except (OSError, PermissionError):
        pass  # Will use default Flask session directory

application = Flask(__name__)
# Set secret key for sessions
application.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

application.config.update(
    SESSION_TYPE="filesystem",
    SESSION_FILE_DIR=session_dir,
    SESSION_PERMANENT=True,
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=10),
    SESSION_REFRESH_EACH_REQUEST=False,
    SESSION_FILE_THRESHOLD=20,
    SESSION_COOKIE_SECURE=False,  # Set to True only if using HTTPS
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)
Session(application)



def require_user_type(allowed_types):
    """בודק אם המשתמש מחובר וסוג המשתמש מורשה"""
    user_type = session.get('user_type')
    if not user_type or user_type not in allowed_types:
        return False
    return True

@application.route("/")
def homepage():
    error = request.args.get('error')
    return render_template('homepage.html', error=error)


@application.route("/login", methods=["POST", "GET"])
def login():
    # If user is already logged in as user or guest, redirect to book_flights
    user_type = session.get('user_type')
    if user_type in ['user', 'guest']:
        return redirect("/book_flights")
    
    if request.method == "POST":
        try:
            email = request.form.get("email")
            password = request.form.get("password")
            stored_password = users.get_password(email)
            if stored_password and stored_password == password:
                session['user_type'] = 'user'
                session['user_email'] = email
                return redirect("/book_flights")
            else:
                return render_template("login.html", message='Incorrect Login Details.')
        except Exception as e:
            print(f"Login error: {e}")
            return render_template("login.html", message='An error occurred. Please try again.')
    error = request.args.get('error')
    message = error if error else None
    return render_template("login.html", message=message)

@application.route("/sign_up", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        birth_date = request.form.get("birth_date")
        passport_number = request.form.get("passport_number")

        # קליטת מחרוזת הטלפונים (למשל: "050-123, 052-456")
        phones_string = request.form.get("phone_numbers")

        # Check if email is already registered as guest
        if guest.is_guest(email):
            return render_template("sign_up.html", 
                                 error="You are already registered as a guest, please use another email",
                                 first_name=first_name,
                                 last_name=last_name,
                                 email=email,
                                 birth_date=birth_date,
                                 passport_number=passport_number,
                                 phone_numbers=phones_string)
        
        # Check if email is already registered as user
        if users.is_user(email):
            return render_template("sign_up.html", 
                                 error="This email is already registered in the system, please log in instead",
                                 first_name=first_name,
                                 last_name=last_name,
                                 email=email,
                                 birth_date=birth_date,
                                 passport_number=passport_number,
                                 phone_numbers=phones_string)

        new_user = User(email, password, first_name, last_name, phones_string, None, birth_date, passport_number)
        try:
            add_user(new_user)
            session['user_type'] = 'user'
            session['user_email'] = email
            return redirect("/book_flights")

        except Exception as e:
            print(f"Error: {e}")
            return render_template("sign_up.html", 
                                 error="Error registering user",
                                 first_name=first_name,
                                 last_name=last_name,
                                 email=email,
                                 birth_date=birth_date,
                                 passport_number=passport_number,
                                 phone_numbers=phones_string)

    return render_template("sign_up.html")


@application.route("/guest", methods=["POST", "GET"])
def guest_page():
    # If user is already logged in as guest or user, redirect to book_flights
    user_type = session.get('user_type')
    if user_type in ['guest', 'user']:
        return redirect("/book_flights")
    
    if request.method == "POST":
        try:
            email = request.form.get("email")
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            phone = request.form.get("phone")

            # שלב א': אם יש רק email -> נבדוק מה הסטטוס שלו
            if email and not (first_name and last_name and phone):
                print(f"Checking guest status for email: {email}")
                # 1. בדיקה האם הוא כבר קיים כאורח
                is_existing_guest = guest.is_guest(email)
                print(f"Is existing guest: {is_existing_guest}")
                if is_existing_guest:
                    session['user_type'] = 'guest'
                    session['user_email'] = email
                    return redirect("/book_flights")
                
                # 2. בדיקה האם הוא קיים כמשתמש רשום
                is_existing_user = users.is_user(email)
                print(f"Is existing user: {is_existing_user}")
                if is_existing_user:
                    return render_template("login.html", message="You are a registered user. Please log in.")
                
                # 3. אם הוא לא אורח ולא רשום -> נטען את הדף עם השדות הפתוחים
                print(f"New guest, showing details form")
                return render_template("guest.html", show_details=True, email_value=email)

            # שלב ב': אם שלחו לנו את כל הפרטים -> ניצור את האורח
            elif email and first_name and last_name and phone:
                # אם הגענו לכאן, זה אומר שהוא לא אורח ולא משתמש (כי זה נבדק בשלב א')
                # אז ניצור אורח חדש
                new_guest = Guest(email, first_name, last_name, [phone])
                guest.add_guest(new_guest)
                session['user_type'] = 'guest'
                session['user_email'] = email
                return redirect("/book_flights")
        except Exception as e:
            import traceback
            print(f"Guest page error: {e}")
            traceback.print_exc()
            email_val = email if 'email' in locals() and email else ''
            return render_template("guest.html", message=f"An error occurred: {str(e)}", email_value=email_val)

    return render_template("guest.html")

@application.route("/manager", methods=["POST", "GET"])
def manager():
    # If manager is already logged in, redirect to dashboard
    user_type = session.get('user_type')
    if user_type == 'manager':
        return redirect("/manager/dashboard")
    
    if request.method == "POST":
        manager_id = request.form.get("manager_id")
        password = request.form.get("password")
        result = data.sql_query("""SELECT password FROM Managers WHERE manager_id = %s""", manager_id)
        if result and len(result) > 0 and result[0][0] == password:
            session['user_type'] = 'manager'
            session['manager_id'] = manager_id
            return redirect("/manager/dashboard")
        else:
            return render_template("manager.html", message='Incorrect Login Details.')
    error = request.args.get('error')
    message = error if error else None
    return render_template("manager.html", message=message)

@application.route("/book_flights", methods=["GET", "POST"])
def book_flights():
    user_type = session.get('user_type')
    
    # Check if user is a manager
    if user_type == 'manager':
        return redirect("/?error=Managers cannot access the booking system. Please use the manager dashboard.")
    
    # Check if user is logged in as user or guest
    if not require_user_type(['user', 'guest']):
        return redirect("/?error=Please log in or continue as guest to search and book flights")
    
    airports = get_all_airports()
    flight_objects = []
    search_params = {}
    show_alternative_flights = False
    
    if request.method == "POST":
        origin = request.form.get("origin")
        destination = request.form.get("destination")
        date = request.form.get("date")
        
        search_params = {
            'origin': origin,
            'destination': destination,
            'date': date
        }
        
        # Check if any filters were applied
        has_filters = bool(origin or destination or date)
        
        # Search with filters
        flight_objects = Flight.get_active_flights(origin=origin if origin else None, 
                                                    destination=destination if destination else None,
                                                    flight_date=date if date else None)
        
        # If no flights found with filters, show alternative flights
        if not flight_objects and has_filters:
            show_alternative_flights = True
            flight_objects = Flight.get_active_flights()
    else:
        # אם זה GET ללא פרמטרים, נציג את כל הטיסות הפעילות
        flight_objects = Flight.get_active_flights()
    
    # המרת Flight objects לפורמט tuple עבור ה-template
    flights_with_images = []
    for flight in flight_objects:
        flight_tuple = (
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
        )
        flights_with_images.append(flight_tuple)
    
    # Check if filters are active
    has_active_filters = bool(search_params.get('origin') or search_params.get('destination') or search_params.get('date'))
    
    return render_template("book_flights.html", 
                         airports=airports, 
                         flights=flights_with_images,
                         search_params=search_params,
                         has_active_filters=has_active_filters,
                         show_alternative_flights=show_alternative_flights)

@application.route("/select_seats/<int:flight_id>", methods=["GET", "POST"])
def select_seats(flight_id):
    user_type = session.get('user_type')
    
    # Check if user is a manager
    if user_type == 'manager':
        return redirect("/?error=Managers cannot access the booking system. Please use the manager dashboard.")
    
    # Check if user is logged in as user or guest
    if not require_user_type(['user', 'guest']):
        return redirect("/?error=Please log in or continue as guest to select seats")
    
    # Get flight object using the Flight class
    flight = Flight.get_flight_by_id(flight_id)
    if not flight:
        return redirect("/book_flights")
    
    # Check if flight is full or cancelled
    if flight.status == 'Full':
        return redirect("/book_flights?error=Flight is full. No seats available.")
    if flight.status == 'Cancelled':
        return redirect("/book_flights?error=Flight has been cancelled.")
    
    # Organize seats by row using the flight object
    seats_by_row = flight.organize_seats_by_row()
    
    # Convert flight object to tuple format for template compatibility
    flight_tuple = (
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
    
    if request.method == "POST":
        # Handle seat selection - save to session and redirect to complete booking
        selected_seats = request.form.getlist('selected_seats')
        if not selected_seats:
            return render_template("select_seats.html", 
                                 flight=flight_tuple,
                                 seats_by_row=seats_by_row,
                                 price_economy=flight.price_economy,
                                 price_business=flight.price_business,
                                 error="Please select at least one seat")
        
        # Create Order object from seat selection
        user_email = session.get('user_email')
        order, error = Order.create_from_seat_selection(flight, selected_seats, user_email)
        
        if error:
            return render_template("select_seats.html", 
                                 flight=flight_tuple,
                                 seats_by_row=seats_by_row,
                                 price_economy=flight.price_economy,
                                 price_business=flight.price_business,
                                 error=error)
        
        # Save order to session
        order.save_to_session(session)
        
        # Redirect to complete booking page
        return redirect(f"/complete_booking/{flight_id}")
    
    return render_template("select_seats.html", 
                         flight=flight_tuple,
                         seats_by_row=seats_by_row,
                         price_economy=flight.price_economy,
                         price_business=flight.price_business)

@application.route("/complete_booking/<int:flight_id>", methods=["GET", "POST"])
def complete_booking(flight_id):
    user_type = session.get('user_type')
    
    # Check if user is a manager
    if user_type == 'manager':
        return redirect("/?error=Managers cannot access the booking system. Please use the manager dashboard.")
    
    # Check if user is logged in as user or guest
    if not require_user_type(['user', 'guest']):
        return redirect("/?error=Please log in or continue as guest to complete booking")
    
    # Get order from session
    order = Order.from_session(session, flight_id)
    if not order:
        return redirect(f"/select_seats/{flight_id}")
    
    user_type = session.get('user_type')
    user_email = session.get('user_email')
    
    if request.method == "POST":
        # Handle form submission
        if user_type == 'guest':
            # For guests: validate form data only (no DB check, no auto-fill)
            # Create temporary guest object just for validation
            temp_guest = guest.Guest(user_email, '', '', [])
            is_valid, error_msg, validated_data = temp_guest.validate_booking_data(request.form)
            
            if not is_valid:
                # Return form with entered values (no DB data)
                user_data = {
                    'first_name': request.form.get("first_name", ''),
                    'last_name': request.form.get("last_name", ''),
                    'passport_number': request.form.get("passport_number", ''),
                    'birth_date': request.form.get("birth_date", ''),
                    'phone_numbers': request.form.get("phone_numbers", '')
                }
                return render_template("complete_booking.html",
                                     flight=order.flight,
                                     booking=order.to_dict(),
                                     user_type=user_type,
                                     user_data=user_data,
                                     error=error_msg)
            
            # Save guest data to order object (NOT saved to DB - only for order confirmation)
            order.user_data = validated_data
        else:  # registered user
            # Get user object and use existing data (user is already logged in)
            user = users.read_user(user_email)
            
            # Set user data in order (from DB, read-only)
            order.user_data = user.get_booking_form_data()
        
        # Save updated order to session
        order.save_to_session(session)
        return redirect(f"/confirm_booking/{flight_id}")
    
    # GET request - show form
    if user_type == 'guest':
        # For guests: empty form (no DB data, no auto-fill)
        user_data = {
            'first_name': '',
            'last_name': '',
            'passport_number': '',
            'birth_date': '',
            'phone_numbers': ''
        }
    else:  # registered user
        # Get user data from database (user is already logged in)
        user = users.read_user(user_email)
        user_data = user.get_booking_form_data()
    
    return render_template("complete_booking.html",
                         flight=order.flight,
                         booking=order.to_dict(),
                         user_type=user_type,
                         user_data=user_data)

@application.route("/confirm_booking/<int:flight_id>", methods=["GET", "POST"])
def confirm_booking(flight_id):
    user_type = session.get('user_type')
    
    # Check if user is a manager
    if user_type == 'manager':
        return redirect("/?error=Managers cannot access the booking system. Please use the manager dashboard.")
    
    # Check if user is logged in as user or guest
    if not require_user_type(['user', 'guest']):
        return redirect("/?error=Please log in or continue as guest to confirm booking")
    
    # Get order from session
    order = Order.from_session(session, flight_id)
    if not order:
        return redirect(f"/select_seats/{flight_id}")
    
    user_type = session.get('user_type')
    user_email = session.get('user_email')
    
    if request.method == "POST":
        # Final confirmation - process the order using Duck Typing
        if user_type == 'guest':
            if not order.user_data:
                return redirect(f"/complete_booking/{flight_id}")
            
            # For guests: create order without checking DB (guest data not saved to DB)
            # Create temporary guest object just for validation
            temp_guest = guest.Guest(user_email, '', '', [])
            
            # Use add_order method - creates order in DB (guest personal data NOT saved to DB)
            order_id, error = temp_guest.add_order(order, order.user_data)
        else:  # registered user
            # Get user object (user is already logged in)
            user = users.read_user(user_email)
            
            # Use add_order method - uses existing user data from DB
            order_id, error = user.add_order(order)
        
        if error:
            confirmation_data = order.get_confirmation_data()
            return render_template("confirm_booking.html",
                                 flight=confirmation_data['flight'],
                                 booking=confirmation_data['booking'],
                                 user_type=user_type,
                                 user_data=confirmation_data['user_data'],
                                 error=error)
        
        # Get confirmation data
        confirmation_data = order.get_confirmation_data()
        confirmation_data['order_id'] = order_id
        
        # Clear order from session
        session.pop('booking', None)
        
        # Redirect to success page or show confirmation
        return render_template("confirm_booking.html",
                             flight=confirmation_data['flight'],
                             booking=confirmation_data['booking'],
                             user_type=user_type,
                             user_data=confirmation_data['user_data'],
                             order_id=order_id,
                             success=True)
    
    # GET request - show confirmation page
    confirmation_data = order.get_confirmation_data()
    return render_template("confirm_booking.html",
                         flight=confirmation_data['flight'],
                         booking=confirmation_data['booking'],
                         user_type=user_type,
                         user_data=confirmation_data['user_data'])

@application.route("/flights_management")
def flights_management():
    if not require_user_type(['manager']):
        return render_template("manager.html", message='Access denied. Please log in as a manager.')
    
    airports = get_all_airports()
    today = date.today().isoformat()
    
    return render_template("flights_management.html", 
                         step=1, 
                         airports=airports, 
                         today=today)

@application.route("/flights_management/select_route", methods=["POST"])
def select_route():
    """Step 1: Process route selection and move to step 2"""
    if not require_user_type(['manager']):
        return redirect("/manager?error=Access denied. Please log in as manager")
    
    origin_airport = request.form.get("origin_airport")
    destination_airport = request.form.get("destination_airport")
    departure_date = request.form.get("departure_date")
    departure_time = request.form.get("departure_time")
    
    if not all([origin_airport, destination_airport, departure_date, departure_time]):
        airports = get_all_airports()
        return render_template("flights_management.html", 
                             step=1,
                             airports=airports,
                             today=date.today().isoformat(),
                             error="Please fill all required fields")
    
    # Get route information
    route_info_result = get_flight_route_info(origin_airport, destination_airport)
    if not route_info_result:
        airports = get_all_airports()
        return render_template("flights_management.html", 
                             step=1,
                             airports=airports,
                             today=date.today().isoformat(),
                             error="Route not found in database")
    
    flight_duration, origin_country, destination_country = route_info_result
    is_long = is_long_flight(flight_duration)
    
    # Calculate duration hours and minutes
    duration_hours = flight_duration // 60
    duration_minutes = flight_duration % 60
    
    route_info = {
        'duration_hours': duration_hours,
        'duration_minutes': duration_minutes,
        'is_long_flight': is_long
    }
    
    # Get available planes
    available_planes = get_available_planes(origin_country, is_long_flight=is_long, 
                                          departure_date=departure_date, 
                                          departure_time=departure_time)
    
    # Get crew requirements
    large_crew = get_crew_requirements('Large', is_long)
    small_crew = get_crew_requirements('Small', is_long)
    
    # Get available pilots and attendants (will be filtered after plane selection)
    available_pilots = get_available_pilots(origin_country, origin_airport=origin_airport,
                                           is_long_flight=is_long,
                                           departure_date=departure_date,
                                           departure_time=departure_time)
    
    available_attendants = get_available_attendants(origin_country, origin_airport=origin_airport,
                                                    is_long_flight=is_long,
                                                    departure_date=departure_date,
                                                    departure_time=departure_time)
    
    return render_template("flights_management.html",
                         step=2,
                         origin_airport=origin_airport,
                         destination_airport=destination_airport,
                         departure_date=departure_date,
                         departure_time=departure_time,
                         route_info=route_info,
                         available_planes=available_planes,
                         large_crew=large_crew,
                         small_crew=small_crew,
                         available_pilots=available_pilots,
                         available_attendants=available_attendants,
                         today=date.today().isoformat())

@application.route("/flights_management/update_plane_selection", methods=["POST"])
def update_plane_selection():
    """Update plane selection and show crew selection"""
    if not require_user_type(['manager']):
        return redirect("/manager?error=Access denied. Please log in as manager")
    
    origin_airport = request.form.get("origin_airport")
    destination_airport = request.form.get("destination_airport")
    departure_date = request.form.get("departure_date")
    departure_time = request.form.get("departure_time")
    plane_id = request.form.get("plane_id")
    
    # Get previously selected crew (if any)
    selected_pilot_ids = request.form.getlist("pilot_ids")
    selected_attendant_ids = request.form.getlist("attendant_ids")
    price_economy = request.form.get("price_economy")
    price_business = request.form.get("price_business")
    
    if not all([origin_airport, destination_airport, departure_date, departure_time]):
        return redirect("/flights_management")
    
    # Get route information
    route_info_result = get_flight_route_info(origin_airport, destination_airport)
    if not route_info_result:
        return redirect("/flights_management")
    
    flight_duration, origin_country, destination_country = route_info_result
    is_long = is_long_flight(flight_duration)
    
    duration_hours = flight_duration // 60
    duration_minutes = flight_duration % 60
    
    route_info = {
        'duration_hours': duration_hours,
        'duration_minutes': duration_minutes,
        'is_long_flight': is_long
    }
    
    # Get available planes
    available_planes = get_available_planes(origin_country, is_long_flight=is_long, 
                                          departure_date=departure_date, 
                                          departure_time=departure_time)
    
    # Get crew requirements
    large_crew = get_crew_requirements('Large', is_long)
    small_crew = get_crew_requirements('Small', is_long)
    
    # Get available pilots and attendants
    available_pilots = get_available_pilots(origin_country, origin_airport=origin_airport,
                                           is_long_flight=is_long,
                                           departure_date=departure_date,
                                           departure_time=departure_time)
    
    available_attendants = get_available_attendants(origin_country, origin_airport=origin_airport,
                                                    is_long_flight=is_long,
                                                    departure_date=departure_date,
                                                    departure_time=departure_time)
    
    # Validate crew selection if plane is selected
    pilot_error = None
    attendant_error = None
    crew_error = None
    
    if plane_id:
        try:
            plane_id_int = int(plane_id)
            selected_plane = next((p for p in available_planes if p[0] == plane_id_int), None)
            if selected_plane:
                plane_size = selected_plane[2]
                crew_reqs = large_crew if plane_size == 'Large' else small_crew
                
                # Check pilot selection
                if len(selected_pilot_ids) > 0 and len(selected_pilot_ids) != crew_reqs['pilots']:
                    pilot_error = f"Please select exactly {crew_reqs['pilots']} pilots"
                
                # Check attendant selection
                if len(selected_attendant_ids) > 0 and len(selected_attendant_ids) != crew_reqs['attendants']:
                    attendant_error = f"Please select exactly {crew_reqs['attendants']} attendants"
        except ValueError:
            pass
    
    return render_template("flights_management.html",
                         step=2,
                         origin_airport=origin_airport,
                         destination_airport=destination_airport,
                         departure_date=departure_date,
                         departure_time=departure_time,
                         route_info=route_info,
                         available_planes=available_planes,
                         selected_plane_id=plane_id,
                         selected_pilot_ids=selected_pilot_ids,
                         selected_attendant_ids=selected_attendant_ids,
                         price_economy=price_economy,
                         price_business=price_business,
                         large_crew=large_crew,
                         small_crew=small_crew,
                         available_pilots=available_pilots,
                         available_attendants=available_attendants,
                         pilot_error=pilot_error,
                         attendant_error=attendant_error,
                         crew_error=crew_error,
                         today=date.today().isoformat())

@application.route("/flights_management/add_flight", methods=["POST"])
def add_flight_route():
    """Add new flight to database"""
    if not require_user_type(['manager']):
        return redirect("/manager?error=Access denied. Please log in as manager")
    
    origin_airport = request.form.get("origin_airport")
    destination_airport = request.form.get("destination_airport")
    departure_date = request.form.get("departure_date")
    departure_time = request.form.get("departure_time")
    plane_id = request.form.get("plane_id")
    price_economy = request.form.get("price_economy")
    price_business = request.form.get("price_business")
    
    # Get pilot and attendant IDs
    pilot_ids = request.form.getlist("pilot_ids")
    attendant_ids = request.form.getlist("attendant_ids")
    
    # Get route information for error handling
    route_info_result = get_flight_route_info(origin_airport, destination_airport)
    if not route_info_result:
        return redirect("/flights_management")
    
    flight_duration, origin_country, destination_country = route_info_result
    is_long = is_long_flight(flight_duration)
    
    duration_hours = flight_duration // 60
    duration_minutes = flight_duration % 60
    
    route_info = {
        'duration_hours': duration_hours,
        'duration_minutes': duration_minutes,
        'is_long_flight': is_long
    }
    
    # Get available planes and crew
    available_planes = get_available_planes(origin_country, is_long_flight=is_long, 
                                          departure_date=departure_date, 
                                          departure_time=departure_time)
    large_crew = get_crew_requirements('Large', is_long)
    small_crew = get_crew_requirements('Small', is_long)
    available_pilots = get_available_pilots(origin_country, origin_airport=origin_airport,
                                           is_long_flight=is_long,
                                           departure_date=departure_date,
                                           departure_time=departure_time)
    available_attendants = get_available_attendants(origin_country, origin_airport=origin_airport,
                                                    is_long_flight=is_long,
                                                    departure_date=departure_date,
                                                    departure_time=departure_time)
    
    if not all([origin_airport, destination_airport, departure_date, departure_time, 
                plane_id, price_economy]):
        crew_error = "Please fill all required fields"
        return render_template("flights_management.html",
                             step=2,
                             origin_airport=origin_airport,
                             destination_airport=destination_airport,
                             departure_date=departure_date,
                             departure_time=departure_time,
                             route_info=route_info,
                             available_planes=available_planes,
                             selected_plane_id=plane_id,
                             selected_pilot_ids=pilot_ids,
                             selected_attendant_ids=attendant_ids,
                             price_economy=price_economy,
                             price_business=price_business,
                             large_crew=large_crew,
                             small_crew=small_crew,
                             available_pilots=available_pilots,
                             available_attendants=available_attendants,
                             crew_error=crew_error,
                             today=date.today().isoformat())
    
    # Convert plane_id to int
    try:
        plane_id_int = int(plane_id)
    except ValueError:
        crew_error = "Invalid plane ID"
        return render_template("flights_management.html",
                             step=2,
                             origin_airport=origin_airport,
                             destination_airport=destination_airport,
                             departure_date=departure_date,
                             departure_time=departure_time,
                             route_info=route_info,
                             available_planes=available_planes,
                             selected_plane_id=plane_id,
                             selected_pilot_ids=pilot_ids,
                             selected_attendant_ids=attendant_ids,
                             price_economy=price_economy,
                             price_business=price_business,
                             large_crew=large_crew,
                             small_crew=small_crew,
                             available_pilots=available_pilots,
                             available_attendants=available_attendants,
                             crew_error=crew_error,
                             today=date.today().isoformat())
    
    # Get plane size for crew validation
    selected_plane = next((p for p in available_planes if p[0] == plane_id_int), None)
    if not selected_plane:
        crew_error = "Selected plane not available"
        return render_template("flights_management.html",
                             step=2,
                             origin_airport=origin_airport,
                             destination_airport=destination_airport,
                             departure_date=departure_date,
                             departure_time=departure_time,
                             route_info=route_info,
                             available_planes=available_planes,
                             selected_plane_id=plane_id,
                             selected_pilot_ids=pilot_ids,
                             selected_attendant_ids=attendant_ids,
                             price_economy=price_economy,
                             price_business=price_business,
                             large_crew=large_crew,
                             small_crew=small_crew,
                             available_pilots=available_pilots,
                             available_attendants=available_attendants,
                             crew_error=crew_error,
                             today=date.today().isoformat())
    
    plane_size = selected_plane[2]
    crew_reqs = large_crew if plane_size == 'Large' else small_crew
    
    # Validate crew selection
    pilot_error = None
    attendant_error = None
    crew_error = None
    
    if len(pilot_ids) != crew_reqs['pilots']:
        pilot_error = f"Please select exactly {crew_reqs['pilots']} pilots"
        crew_error = f"Please select exactly {crew_reqs['pilots']} pilots and {crew_reqs['attendants']} attendants"
    
    if len(attendant_ids) != crew_reqs['attendants']:
        attendant_error = f"Please select exactly {crew_reqs['attendants']} attendants"
        if not crew_error:
            crew_error = f"Please select exactly {crew_reqs['pilots']} pilots and {crew_reqs['attendants']} attendants"
    
    if crew_error:
        return render_template("flights_management.html",
                             step=2,
                             origin_airport=origin_airport,
                             destination_airport=destination_airport,
                             departure_date=departure_date,
                             departure_time=departure_time,
                             route_info=route_info,
                             available_planes=available_planes,
                             selected_plane_id=plane_id,
                             selected_pilot_ids=pilot_ids,
                             selected_attendant_ids=attendant_ids,
                             price_economy=price_economy,
                             price_business=price_business,
                             large_crew=large_crew,
                             small_crew=small_crew,
                             available_pilots=available_pilots,
                             available_attendants=available_attendants,
                             pilot_error=pilot_error,
                             attendant_error=attendant_error,
                             crew_error=crew_error,
                             today=date.today().isoformat())
    
    # Convert prices to float
    try:
        price_economy = float(price_economy)
        price_business = float(price_business) if price_business else None
    except ValueError:
        crew_error = "Invalid price format"
        return render_template("flights_management.html",
                             step=2,
                             origin_airport=origin_airport,
                             destination_airport=destination_airport,
                             departure_date=departure_date,
                             departure_time=departure_time,
                             route_info=route_info,
                             available_planes=available_planes,
                             selected_plane_id=plane_id,
                             selected_pilot_ids=pilot_ids,
                             selected_attendant_ids=attendant_ids,
                             price_economy=price_economy,
                             price_business=price_business,
                             large_crew=large_crew,
                             small_crew=small_crew,
                             available_pilots=available_pilots,
                             available_attendants=available_attendants,
                             crew_error=crew_error,
                             today=date.today().isoformat())
    
    # Add flight using the function from flights.py
    success, flight_id, error_message = add_flight(
        departure_date=departure_date,
        departure_time=departure_time,
        origin_airport=origin_airport,
        destination_airport=destination_airport,
        plane_id=plane_id_int,
        pilot_ids=pilot_ids,
        attendant_ids=attendant_ids,
        price_economy=price_economy,
        price_business=price_business
    )
    
    if success:
        return render_template("flights_management.html",
                             step=1,
                             airports=get_all_airports(),
                             today=date.today().isoformat(),
                             success=True,
                             flight_id=flight_id)
    else:
        # Return to step 2 with error message
        crew_error = error_message
        return render_template("flights_management.html",
                             step=2,
                             origin_airport=origin_airport,
                             destination_airport=destination_airport,
                             departure_date=departure_date,
                             departure_time=departure_time,
                             route_info=route_info,
                             available_planes=available_planes,
                             selected_plane_id=str(plane_id_int),
                             selected_pilot_ids=pilot_ids,
                             selected_attendant_ids=attendant_ids,
                             price_economy=str(price_economy),
                             price_business=str(price_business) if price_business else None,
                             large_crew=large_crew,
                             small_crew=small_crew,
                             available_pilots=available_pilots,
                             available_attendants=available_attendants,
                             crew_error=crew_error,
                             today=date.today().isoformat())

@application.route("/manage_orders", methods=["GET", "POST"])
def manage_orders():
    """Order management page for guests - requires order number"""
    user_type = session.get('user_type')
    
    # Check if user is a manager
    if user_type == 'manager':
        return redirect("/?error=Managers cannot access the booking system. Please use the manager dashboard.")
    
    # Allow guests and users to access this page
    if not require_user_type(['user', 'guest']):
        return redirect("/?error=Please log in or continue as guest to manage orders")
    
    if request.method == "POST":
        order_id = request.form.get("order_id")
        if not order_id:
            return render_template("manage_orders.html", error="Please enter order number")
        
        try:
            order_id = int(order_id)
        except ValueError:
            return render_template("manage_orders.html", error="Invalid order number")
        
        order = Order.get_by_id(order_id)
        if not order:
            return render_template("manage_orders.html", error="Order not found")
        
        # Verify that the order belongs to the current user/guest
        user_email = session.get('user_email')
        if order.email != user_email:
            return render_template("manage_orders.html", error="You don't have access to this order")
        
        # Get display status
        status, cancellation_fee, final_price = order.get_display_status()
        
        return render_template("order_details.html",
                             order=order,
                             display_status=status,
                             cancellation_fee=cancellation_fee,
                             final_price=final_price,
                             is_guest=True)
    
    return render_template("manage_orders.html")

@application.route("/my_orders")
def my_orders():
    """Order management page for registered users - shows all orders"""
    if not require_user_type(['user']):
        return redirect("/login?error=Please log in as a registered user to view your orders")
    
    user_email = session.get('user_email')
    orders = Order.get_by_email(user_email)
    
    # Get display status for each order
    orders_with_status = []
    for order in orders:
        status, cancellation_fee, final_price = order.get_display_status()
        orders_with_status.append({
            'order': order,
            'display_status': status,
            'cancellation_fee': cancellation_fee,
            'final_price': final_price
        })
    
    return render_template("my_orders.html", orders=orders_with_status)

@application.route("/order_details/<int:order_id>")
def order_details(order_id):
    """View order details"""
    user_type = session.get('user_type')
    
    # Check if user is a manager
    if user_type == 'manager':
        return redirect("/?error=Managers cannot access the booking system. Please use the manager dashboard.")
    
    # Check if user is logged in as user or guest
    if not require_user_type(['user', 'guest']):
        return redirect("/?error=Please log in or continue as guest to view order details")
    
    user_type = session.get('user_type')
    user_email = session.get('user_email')
    
    order = Order.get_by_id(order_id)
    if not order:
        return render_template("error.html", error="Order not found")
    
    # Verify that the order belongs to the current user/guest
    if order.email != user_email:
        return render_template("error.html", error="You don't have access to this order")
    
    # Get display status
    status, _, final_price = order.get_display_status()
    
    # Calculate cancellation fee - use from status if cancelled, otherwise calculate for active orders
    if status == 'Cancelled by Customer':
        cancellation_fee = order.total_payment * 0.05
    elif status == 'Active':
        cancellation_fee = order.get_cancellation_fee()
    else:
        cancellation_fee = 0.0
    
    is_guest = (user_type == 'guest')
    
    return render_template("order_details.html",
                         order=order,
                         display_status=status,
                         cancellation_fee=cancellation_fee,
                         final_price=final_price,
                         is_guest=is_guest)

@application.route("/confirm_cancel/<int:order_id>")
def confirm_cancel(order_id):
    """Confirmation page before cancelling an order"""
    user_type = session.get('user_type')
    
    # Check if user is a manager
    if user_type == 'manager':
        return redirect("/?error=Managers cannot access the booking system. Please use the manager dashboard.")
    
    # Check if user is logged in as user or guest
    if not require_user_type(['user', 'guest']):
        return redirect("/?error=Please log in or continue as guest to cancel order")
    
    user_type = session.get('user_type')
    user_email = session.get('user_email')
    
    order = Order.get_by_id(order_id)
    if not order:
        return render_template("error.html", error="Order not found")
    
    # Verify that the order belongs to the current user/guest
    if order.email != user_email:
        return render_template("error.html", error="You don't have access to this order")
    
    # Check if order can be cancelled
    status, _, _ = order.get_display_status()
    if status != 'Active':
        return render_template("error.html", error="Order cannot be cancelled")
    
    # Calculate cancellation fee (5% of total payment) for active orders
    cancellation_fee = order.get_cancellation_fee()
    
    is_guest = (user_type == 'guest')
    
    return render_template("confirm_cancel.html",
                         order=order,
                         cancellation_fee=cancellation_fee,
                         is_guest=is_guest)

@application.route("/cancel_order/<int:order_id>", methods=["POST"])
def cancel_order(order_id):
    """Cancel an order"""
    user_type = session.get('user_type')
    
    # Check if user is a manager
    if user_type == 'manager':
        return redirect("/?error=Managers cannot access the booking system. Please use the manager dashboard.")
    
    # Check if user is logged in as user or guest
    if not require_user_type(['user', 'guest']):
        return redirect("/?error=Please log in or continue as guest to cancel order")
    
    user_type = session.get('user_type')
    user_email = session.get('user_email')
    
    order = Order.get_by_id(order_id)
    if not order:
        return render_template("error.html", error="Order not found")
    
    # Verify that the order belongs to the current user/guest
    if order.email != user_email:
        return render_template("error.html", error="You don't have access to this order")
    
    # Check if order can be cancelled
    status, cancellation_fee, _ = order.get_display_status()
    if status != 'Active':
        return render_template("error.html", error="Order cannot be cancelled")
    
    # Cancel the order
    success, error_msg = order.cancel_by_customer()
    if not success:
        return render_template("error.html", error=error_msg)
    
    # Reload order to get updated status
    order = Order.get_by_id(order_id)
    status, cancellation_fee, final_price = order.get_display_status()
    
    # Redirect based on user type
    if user_type == 'guest':
        return render_template("order_details.html",
                             order=order, display_status=status,
                             cancellation_fee=cancellation_fee,
                             final_price=final_price, is_guest=True,
                             cancelled=True)
    else:
        return redirect("/my_orders")

@application.route("/manager/dashboard", methods=["GET", "POST"])
def manager_dashboard():
    """Manager dashboard - shows all flights with optional filtering"""
    if not require_user_type(['manager']):
        return redirect("/manager?error=Access denied. Please log in as manager")
    
    # Get filter parameters from request (works for both GET and POST)
    filter_date = request.form.get("filter_date") or request.args.get("filter_date")
    filter_origin = request.form.get("filter_origin") or request.args.get("filter_origin")
    filter_destination = request.form.get("filter_destination") or request.args.get("filter_destination")
    filter_status = request.form.get("filter_status") or request.args.get("filter_status")
    
    # Get all airports for filter dropdowns
    airports = get_all_airports()
    
    # Build query with optional filters
    # For "Full" status, we need to check dynamically if flight has no available seats
    query = """
        SELECT f.flight_id, f.departure_time, f.departure_date, f.origin_airport_name,
            f.destination_airport_name, f.plane_id, f.status, ao.city as origin_city,
            ao.country as origin_country, ad.city as destination_city,
            ad.country as destination_country,
            CASE 
                WHEN TIMESTAMPDIFF(HOUR, NOW(), CONCAT(f.departure_date, ' ', f.departure_time)) > 72 
                THEN 1 
                ELSE 0 
            END as can_cancel,
            (SELECT COUNT(*) FROM Seats s WHERE s.plane_id = f.plane_id) as total_seats,
            (SELECT COUNT(*) FROM FlightTickets ft WHERE ft.flight_id = f.flight_id) as booked_seats
        FROM Flights f
        JOIN Airports ao ON f.origin_airport_name = ao.airport_name
        JOIN Airports ad ON f.destination_airport_name = ad.airport_name
        WHERE 1=1
    """
    
    params = []
    
    # Add filters if provided
    if filter_date:
        query += " AND f.departure_date = %s"
        params.append(filter_date)
    
    if filter_origin:
        query += " AND f.origin_airport_name = %s"
        params.append(filter_origin)
    
    if filter_destination:
        query += " AND f.destination_airport_name = %s"
        params.append(filter_destination)
    
    if filter_status:
        if filter_status == 'Full':
            # For "Full" status, check if all seats are booked (status is 'Full' OR status is 'Active' and no seats available)
            query += """ AND (
                f.status = 'Full' 
                OR (
                    f.status = 'Active' 
                    AND (SELECT COUNT(*) FROM Seats s WHERE s.plane_id = f.plane_id) = 
                        (SELECT COUNT(*) FROM FlightTickets ft WHERE ft.flight_id = f.flight_id)
                )
            )"""
        else:
            query += " AND f.status = %s"
            params.append(filter_status)
    
    query += " ORDER BY f.departure_date DESC, f.departure_time DESC"
    
    try:
        flights = data.sql_query(query, *params)
    except Exception as e:
        print(f"Error fetching flights: {str(e)}")
        flights = []
    
    # Prepare filter values for template (to keep form values after submission)
    filter_values = {
        'date': filter_date or '',
        'origin': filter_origin or '',
        'destination': filter_destination or '',
        'status': filter_status or ''
    }
    
    return render_template("manager_dashboard.html", 
                        flights=flights, 
                        airports=airports,
                        filter_values=filter_values)

@application.route("/manager/add_plane", methods=["GET", "POST"])
def add_plane():
    """Add a new plane to the fleet - two step process"""
    if not require_user_type(['manager']):
        return redirect("/manager?error=Access denied. Please log in as manager")
    
    step = request.args.get('step', '1')
    
    if request.method == "POST":
        # Step 1: Plane basic details
        if step == '1':
            plane_id = request.form.get("plane_id")
            manufacturer = request.form.get("manufacturer")
            size = request.form.get("size")
            purchase_date = request.form.get("purchase_date")
            
            # Validate all fields are provided
            if not all([plane_id, manufacturer, size, purchase_date]):
                return render_template("add_plane.html", 
                                     step=1,
                                     error="Please fill all required fields",
                                     plane_id=plane_id or "",
                                     manufacturer=manufacturer or "",
                                     size=size or "",
                                     purchase_date=purchase_date or "")
            
            # Validate manufacturer
            valid_manufacturers = ['Boeing', 'Airbus', 'Dassault']
            if manufacturer not in valid_manufacturers:
                return render_template("add_plane.html",
                                     step=1,
                                     error="Invalid manufacturer. Please select Boeing, Airbus, or Dassault",
                                     plane_id=plane_id,
                                     manufacturer=manufacturer,
                                     size=size,
                                     purchase_date=purchase_date)
            
            # Validate size
            valid_sizes = ['Large', 'Small']
            if size not in valid_sizes:
                return render_template("add_plane.html",
                                     step=1,
                                     error="Invalid size. Please select Large or Small",
                                     plane_id=plane_id,
                                     manufacturer=manufacturer,
                                     size=size,
                                     purchase_date=purchase_date)
            
            # Validate plane_id is numeric
            try:
                plane_id_int = int(plane_id)
            except ValueError:
                return render_template("add_plane.html",
                                     step=1,
                                     error="Plane ID must be a number",
                                     plane_id=plane_id,
                                     manufacturer=manufacturer,
                                     size=size,
                                     purchase_date=purchase_date)
            
            # Check if plane_id already exists
            existing_plane = data.sql_query("SELECT plane_id FROM Planes WHERE plane_id = %s", plane_id_int)
            if existing_plane:
                return render_template("add_plane.html",
                                     step=1,
                                     error=f"Plane with ID {plane_id_int} already exists",
                                     plane_id=plane_id,
                                     manufacturer=manufacturer,
                                     size=size,
                                     purchase_date=purchase_date)
            
            # Insert plane into database
            try:
                data.sql_insert(
                    "INSERT INTO Planes (plane_id, manufacturer, size, purchase_date) VALUES (%s, %s, %s, %s)",
                    plane_id_int, manufacturer, size, purchase_date
                )
                # Move to step 2 - seat configuration
                return render_template("add_plane.html",
                                     step=2,
                                     plane_id=plane_id_int,
                                     size=size,
                                     manufacturer=manufacturer,
                                     purchase_date=purchase_date)
            except Exception as e:
                return render_template("add_plane.html",
                                     step=1,
                                     error=f"Error adding plane: {str(e)}",
                                     plane_id=plane_id,
                                     manufacturer=manufacturer,
                                     size=size,
                                     purchase_date=purchase_date)
        
        # Step 2: Seat configuration
        elif step == '2':
            plane_id = request.form.get("plane_id")
            size = request.form.get("size")
            
            try:
                plane_id_int = int(plane_id)
            except ValueError:
                return redirect("/manager/add_plane?step=1")
            
            # Validate plane exists
            existing_plane = data.sql_query("SELECT plane_id FROM Planes WHERE plane_id = %s", plane_id_int)
            if not existing_plane:
                return redirect("/manager/add_plane?step=1")
            
            # Get seat configuration based on plane size
            if size == 'Small':
                # Small plane: only Economy class
                economy_rows = request.form.get("economy_rows")
                economy_seats_per_row = request.form.get("economy_seats_per_row")
                
                if not all([economy_rows, economy_seats_per_row]):
                    return render_template("add_plane.html",
                                         step=2,
                                         plane_id=plane_id_int,
                                         size=size,
                                         error="Please fill all required fields",
                                         economy_rows=economy_rows or "",
                                         economy_seats_per_row=economy_seats_per_row or "")
                
                try:
                    economy_rows_int = int(economy_rows)
                    economy_seats_int = int(economy_seats_per_row)
                    
                    if economy_rows_int <= 0 or economy_seats_int <= 0:
                        return render_template("add_plane.html",
                                             step=2,
                                             plane_id=plane_id_int,
                                             size=size,
                                             error="Rows and seats per row must be positive numbers",
                                             economy_rows=economy_rows,
                                             economy_seats_per_row=economy_seats_per_row)
                    
                    # Insert seats for Economy class
                    for row in range(1, economy_rows_int + 1):
                        for col in range(1, economy_seats_int + 1):
                            data.sql_insert(
                                "INSERT INTO Seats (plane_id, seat_row, seat_column, seat_class) VALUES (%s, %s, %s, %s)",
                                plane_id_int, row, col, 'Economy'
                            )
                    
                    return render_template("add_plane.html",
                                         step=3,
                                         success=True,
                                         plane_id=plane_id_int)
                    
                except ValueError:
                    return render_template("add_plane.html",
                                         step=2,
                                         plane_id=plane_id_int,
                                         size=size,
                                         error="Rows and seats per row must be numbers",
                                         economy_rows=economy_rows,
                                         economy_seats_per_row=economy_seats_per_row)
            
            else:  # Large plane: Business and Economy classes
                business_rows = request.form.get("business_rows")
                business_seats_per_row = request.form.get("business_seats_per_row")
                economy_rows = request.form.get("economy_rows")
                economy_seats_per_row = request.form.get("economy_seats_per_row")
                
                if not all([business_rows, business_seats_per_row, economy_rows, economy_seats_per_row]):
                    return render_template("add_plane.html",
                                         step=2,
                                         plane_id=plane_id_int,
                                         size=size,
                                         error="Please fill all required fields",
                                         business_rows=business_rows or "",
                                         business_seats_per_row=business_seats_per_row or "",
                                         economy_rows=economy_rows or "",
                                         economy_seats_per_row=economy_seats_per_row or "")
                
                try:
                    business_rows_int = int(business_rows)
                    business_seats_int = int(business_seats_per_row)
                    economy_rows_int = int(economy_rows)
                    economy_seats_int = int(economy_seats_per_row)
                    
                    if (business_rows_int <= 0 or business_seats_int <= 0 or 
                        economy_rows_int <= 0 or economy_seats_int <= 0):
                        return render_template("add_plane.html",
                                             step=2,
                                             plane_id=plane_id_int,
                                             size=size,
                                             error="Rows and seats per row must be positive numbers",
                                             business_rows=business_rows,
                                             business_seats_per_row=business_seats_per_row,
                                             economy_rows=economy_rows,
                                             economy_seats_per_row=economy_seats_per_row)
                    
                    # Insert seats for Business class
                    for row in range(1, business_rows_int + 1):
                        for col in range(1, business_seats_int + 1):
                            data.sql_insert(
                                "INSERT INTO Seats (plane_id, seat_row, seat_column, seat_class) VALUES (%s, %s, %s, %s)",
                                plane_id_int, row, col, 'Business'
                            )
                    
                    # Insert seats for Economy class (starting after business rows)
                    # Using row numbers starting after business rows (e.g., if business has 4 rows, economy starts at row 10)
                    economy_start_row = max(business_rows_int + 1, 10)  # Start economy at row 10 or after business rows
                    for row in range(economy_start_row, economy_start_row + economy_rows_int):
                        for col in range(1, economy_seats_int + 1):
                            data.sql_insert(
                                "INSERT INTO Seats (plane_id, seat_row, seat_column, seat_class) VALUES (%s, %s, %s, %s)",
                                plane_id_int, row, col, 'Economy'
                            )
                    
                    return render_template("add_plane.html",
                                         step=3,
                                         success=True,
                                         plane_id=plane_id_int)
                    
                except ValueError:
                    return render_template("add_plane.html",
                                         step=2,
                                         plane_id=plane_id_int,
                                         size=size,
                                         error="Rows and seats per row must be numbers",
                                         business_rows=business_rows,
                                         business_seats_per_row=business_seats_per_row,
                                         economy_rows=economy_rows,
                                         economy_seats_per_row=economy_seats_per_row)
                except Exception as e:
                    return render_template("add_plane.html",
                                         step=2,
                                         plane_id=plane_id_int,
                                         size=size,
                                         error=f"Error adding seats: {str(e)}",
                                         business_rows=business_rows,
                                         business_seats_per_row=business_seats_per_row,
                                         economy_rows=economy_rows,
                                         economy_seats_per_row=economy_seats_per_row)
    
    # GET request - show form
    if step == '2':
        # Should not reach here via GET for step 2, redirect to step 1
        return redirect("/manager/add_plane?step=1")
    
    return render_template("add_plane.html",
                         step=1,
                         plane_id="",
                         manufacturer="",
                         size="",
                         purchase_date="")

@application.route("/manager/reports")
def manager_reports():
    """Manager reports page - shows analytics and charts"""
    if not require_user_type(['manager']):
        return redirect("/manager?error=Access denied. Please log in as manager")
    
    # Get all reports data
    reports_data = reports.get_all_reports()
    
    # Create charts
    charts = reports.create_charts(reports_data)
    
    # Prepare data for template
    return render_template("manager_reports.html",
                         avg_tickets=reports_data['avg_tickets'],
                         revenue_by_class=reports_data['revenue_by_class'],
                         pilots_hours=reports_data['employee_hours']['pilots'],
                         attendants_hours=reports_data['employee_hours']['attendants'],
                         total_orders=reports_data['total_orders'],
                         active_flights=reports_data['active_flights'],
                         total_passengers=reports_data['total_passengers'],
                         charts=charts)

@application.route("/manager/confirm_cancel_flight/<int:flight_id>")
def confirm_cancel_flight(flight_id):
    """Confirmation page before cancelling a flight"""
    if not require_user_type(['manager']):
        return redirect("/manager?error=Access denied. Please log in as manager")
    
    flight = Flight.get_flight_by_id(flight_id, include_all_statuses=True)
    if not flight:
        return render_template("error.html", error="Flight not found")
    
    # Prepare flight data for template
    flight_data = {
        'flight_id': flight.flight_id,
        'departure_date': flight.departure_date,
        'departure_time': flight.departure_time,
        'origin': flight.origin_airport,
        'destination': flight.destination_airport,
        'origin_city': flight.origin_city,
        'destination_city': flight.destination_city
    }
    
    return render_template("confirm_cancel_flight.html", flight=flight_data)

@application.route("/manager/cancel_flight/<int:flight_id>", methods=["POST"])
def cancel_flight(flight_id):
    """Cancel a flight"""
    if not require_user_type(['manager']):
        return redirect("/manager?error=Access denied. Please log in as manager")
    
    flight = Flight.get_flight_by_id(flight_id, include_all_statuses=True)
    if not flight:
        return render_template("error.html", error="Flight not found")
    
    if flight.status == 'Cancelled':
        return redirect("/manager/dashboard")
    
    # Cancel the flight
    success, error_msg = flight.cancel_flight()
    if not success:
        return render_template("error.html", error=error_msg)
    
    return redirect("/manager/dashboard")

@application.route("/manager/add_employee", methods=["GET", "POST"])
def add_employee():
    """Add a new employee (Attendant or Pilot)"""
    if not require_user_type(['manager']):
        return redirect("/manager?error=Access denied. Please log in as manager")
    
    if request.method == "POST":
        employee_role = request.form.get("employee_role")
        employee_id = request.form.get("employee_id")
        first_name_he = request.form.get("first_name_he")
        last_name_he = request.form.get("last_name_he")
        phone_number = request.form.get("phone_number")
        city = request.form.get("city")
        street = request.form.get("street")
        house_number = request.form.get("house_number")
        start_work_date = request.form.get("start_work_date")
        long_flight_certified = request.form.get("long_flight_certified")
        
        # Validate all fields are provided
        if not all([employee_role, employee_id, first_name_he, last_name_he, phone_number, 
                   city, street, house_number, start_work_date]):
            return render_template("add_employee.html",
                                 error="Please fill all required fields",
                                 employee_role=employee_role or "",
                                 employee_id=employee_id or "",
                                 first_name_he=first_name_he or "",
                                 last_name_he=last_name_he or "",
                                 phone_number=phone_number or "",
                                 city=city or "",
                                 street=street or "",
                                 house_number=house_number or "",
                                 start_work_date=start_work_date or "",
                                 long_flight_certified=long_flight_certified or "0")
        
        # Validate employee role
        if employee_role not in ['Attendant', 'Pilot']:
            return render_template("add_employee.html",
                                 error="Invalid employee role. Please select Attendant or Pilot",
                                 employee_role=employee_role,
                                 employee_id=employee_id,
                                 first_name_he=first_name_he,
                                 last_name_he=last_name_he,
                                 phone_number=phone_number,
                                 city=city,
                                 street=street,
                                 house_number=house_number,
                                 start_work_date=start_work_date,
                                 long_flight_certified=long_flight_certified or "0")
        
        # Convert long_flight_certified to 0 or 1
        # If checkbox is not checked, it won't be in the form data, so it defaults to 0
        long_flight_certified_int = 1 if long_flight_certified == "1" else 0
        
        # Check if employee ID already exists in the appropriate table
        if employee_role == 'Attendant':
            existing_employee = data.sql_query("SELECT attendant_id FROM Attendants WHERE attendant_id = %s", employee_id)
            table_name = "Attendants"
            id_column = "attendant_id"
        else:  # Pilot
            existing_employee = data.sql_query("SELECT pilot_id FROM Pilots WHERE pilot_id = %s", employee_id)
            table_name = "Pilots"
            id_column = "pilot_id"
        
        if existing_employee:
            return render_template("add_employee.html",
                                 error=f"{employee_role} with ID {employee_id} already exists",
                                 employee_role=employee_role,
                                 employee_id=employee_id,
                                 first_name_he=first_name_he,
                                 last_name_he=last_name_he,
                                 phone_number=phone_number,
                                 city=city,
                                 street=street,
                                 house_number=house_number,
                                 start_work_date=start_work_date,
                                 long_flight_certified=long_flight_certified)
        
        # Insert employee into database
        try:
            if employee_role == 'Attendant':
                data.sql_insert(
                    """INSERT INTO Attendants (attendant_id, first_name_he, last_name_he, phone_number, 
                       city, street, house_number, start_work_date, long_flight_certified) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    employee_id, first_name_he, last_name_he, phone_number,
                    city, street, house_number, start_work_date, long_flight_certified_int
                )
            else:  # Pilot
                data.sql_insert(
                    """INSERT INTO Pilots (pilot_id, first_name_he, last_name_he, phone_number, 
                       city, street, house_number, start_work_date, long_flight_certified) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    employee_id, first_name_he, last_name_he, phone_number,
                    city, street, house_number, start_work_date, long_flight_certified_int
                )
            
            return render_template("add_employee.html",
                                 success=True,
                                 employee_role="",
                                 employee_id="",
                                 first_name_he="",
                                 last_name_he="",
                                 phone_number="",
                                 city="",
                                 street="",
                                 house_number="",
                                 start_work_date="",
                                 long_flight_certified="0")
        except Exception as e:
            return render_template("add_employee.html",
                                 error=f"Error adding employee: {str(e)}",
                                 employee_role=employee_role,
                                 employee_id=employee_id,
                                 first_name_he=first_name_he,
                                 last_name_he=last_name_he,
                                 phone_number=phone_number,
                                 city=city,
                                 street=street,
                                 house_number=house_number,
                                 start_work_date=start_work_date,
                                 long_flight_certified=long_flight_certified)
    
    # GET request - show form
    return render_template("add_employee.html",
                         employee_role="",
                         employee_id="",
                         first_name_he="",
                         last_name_he="",
                         phone_number="",
                         city="",
                         street="",
                         house_number="",
                         start_work_date="",
                         long_flight_certified="0")

@application.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@application.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors - Page Not Found"""
    return render_template("page_not_found.html"), 404


if __name__ == "__main__":
    application.run(debug=True, port=5001)
