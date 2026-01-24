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
import validations

#set up session directory
session_dir = os.path.join(os.getcwd(), "flask_session_data")
try:
    if not os.path.exists(session_dir):
        os.makedirs(session_dir, exist_ok=True)
except (OSError, PermissionError) as e:
    session_dir = "/tmp/flask_session_data"
    try:
        os.makedirs(session_dir, exist_ok=True)
    except (OSError, PermissionError):
        pass

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
    SESSION_COOKIE_SECURE=False,  # Set False because we are not using HTTPS
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)
Session(application)



def require_user_type(allowed_types):
    #Checks if the user is logged in and if the user type is allowed
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
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "").strip()
            
            # Validate email
            is_valid, error = validations.validate_email(email)
            if not is_valid:
                return render_template("login.html", message=error)
            
            #Get the password from the database
            stored_password = users.get_password(email)
            #Check if the password is correct
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
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        birth_date = request.form.get("birth_date", "").strip()
        passport_number = request.form.get("passport_number", "").strip()
        phones_string = request.form.get("phone_numbers", "").strip()

        # Validate email
        is_valid, error = validations.validate_email(email)
        if not is_valid:
            return render_template("sign_up.html", 
                                 error=error,
                                 first_name=first_name,
                                 last_name=last_name,
                                 email=email,
                                 birth_date=birth_date,
                                 passport_number=passport_number,
                                 phone_numbers=phones_string)
        
        # Validate passport number
        is_valid, error = validations.validate_passport_number(passport_number)
        if not is_valid:
            return render_template("sign_up.html", 
                                 error=error,
                                 first_name=first_name,
                                 last_name=last_name,
                                 email=email,
                                 birth_date=birth_date,
                                 passport_number=passport_number,
                                 phone_numbers=phones_string)
        
        # Validate phone numbers
        is_valid, error = validations.validate_phone_number(phones_string)
        if not is_valid:
            return render_template("sign_up.html", 
                                 error=error,
                                 first_name=first_name,
                                 last_name=last_name,
                                 email=email,
                                 birth_date=birth_date,
                                 passport_number=passport_number,
                                 phone_numbers=phones_string)

        # Check if email is already registered as a registered user
        if users.is_registered_user(email):
            return render_template("sign_up.html", 
                                 error="You are already registered to the system, please login",
                                 first_name=first_name,
                                 last_name=last_name,
                                 email=email,
                                 birth_date=birth_date,
                                 passport_number=passport_number,
                                 phone_numbers=phones_string)
        
        # Check if email is already registered as guest
        if guest.is_guest(email):
            return render_template("sign_up.html", 
                                 error="You are registered as a guest, either register with another email or login as a guest",
                                 first_name=first_name,
                                 last_name=last_name,
                                 email=email,
                                 birth_date=birth_date,
                                 passport_number=passport_number,
                                 phone_numbers=phones_string)

        new_user = User(email, password, first_name, last_name, phones_string, None, birth_date, passport_number)
        try:
            #Add the user to the database
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
            email = request.form.get("email", "").strip()
            first_name = request.form.get("first_name", "").strip()
            last_name = request.form.get("last_name", "").strip()
            phone = request.form.get("phone", "").strip()

            #If there is only email, check if the email is valid
            if email and not (first_name and last_name and phone):
                # Validate email
                is_valid, error = validations.validate_email(email)
                if not is_valid:
                    return render_template("guest.html", message=error, email_value=email)
                
                # 1. Check if the email is already registered as a guest
                is_existing_guest = guest.is_guest(email)
                if is_existing_guest:
                    #If the email is already registered as a guest, log them in and redirect to book_flights
                    session['user_type'] = 'guest'
                    session['user_email'] = email
                    return redirect("/book_flights")
                
                # 2. Check if the email is already registered as a registered user
                is_existing_user = users.is_registered_user(email)
                if is_existing_user:
                    #If the email is already registered as a registered user, redirect to login page
                    return render_template("login.html", message="You are a registered user. Please log in.")
                
                # 3. If the email is not registered as a guest or a registered user, show the details form
                return render_template("guest.html", show_details=True, email_value=email)

            # If all details are provided, create the guest
            elif email and first_name and last_name and phone:
                # Validate email
                is_valid, error = validations.validate_email(email)
                if not is_valid:
                    return render_template("guest.html", message=error, show_details=True, email_value=email,
                                         first_name=first_name, last_name=last_name, phone=phone)
                
                # Validate phone number
                is_valid, error = validations.validate_phone_number(phone)
                if not is_valid:
                    return render_template("guest.html", message=error, show_details=True, email_value=email,
                                         first_name=first_name, last_name=last_name, phone=phone)
                
                # Check if email is already registered as guest
                if guest.is_guest(email):
                    # If already a guest, just log them in and redirect
                    session['user_type'] = 'guest'
                    session['user_email'] = email
                    return redirect("/book_flights")
                
                # Check if email is already registered as a registered user
                if users.is_registered_user(email):
                    return render_template("guest.html", 
                                         message="You are a registered user. Please log in.",
                                         show_details=True, email_value=email,
                                         first_name=first_name, last_name=last_name, phone=phone)
                
                # Create new guest
                new_guest = Guest(email, first_name, last_name, [phone])
                #Add the guest to the database
                success = guest.add_guest(new_guest)
                if not success:
                    #If the guest is not added to the database, show an error
                    return render_template("guest.html", 
                                         message="An error occurred. Please try again.",
                                         show_details=True, email_value=email,
                                         first_name=first_name, last_name=last_name, phone=phone)
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
        manager_id = request.form.get("manager_id", "").strip()
        password = request.form.get("password", "").strip()
        
        # Validate manager ID
        is_valid, error = validations.validate_id_number(manager_id)
        if not is_valid:
            return render_template("manager.html", message=error)
        
        #Get the password from the database
        stored_manager_password = data.sql_query("""SELECT password FROM Managers WHERE manager_id = %s""", manager_id)
        #Check if the password is correct
        if stored_manager_password and stored_manager_password == password:
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
    
    # Check if user is logged in as user or guest and if not, redirect to login page
    if not require_user_type(['user', 'guest']):
        return redirect("/?error=Please log in or continue as guest to search and book flights")
    
    airports = get_all_airports() #gets all the airports from the database
    flight_objects = [] 
    search_params = {} #dictionary to store the search parameters
    show_alternative_flights = False 
    
    if request.method == "POST":
        origin = request.form.get("origin") 
        destination = request.form.get("destination") 
        date = request.form.get("date") 
        
        search_params = {'origin': origin,'destination': destination,'date': date}
        
        # Check if any filters were applied
        has_filters = bool((origin and origin.strip()) or 
                           (destination and destination.strip()) or 
                           (date and date.strip()))
        
        # Search with filters
        flight_objects = Flight.get_active_flights(origin=origin if origin else None, 
                                                    destination=destination if destination else None,
                                                    flight_date=date if date else None)
        
        # If no flights found with filters, show alternative flights
        if not flight_objects and has_filters:
            show_alternative_flights = True
            flight_objects = Flight.get_active_flights()
    else:
        # If it is GET without parameters, show all active flights
        flight_objects = Flight.get_active_flights()
    
    # Convert Flight objects to tuple format for the template
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
    
    # Check if filters are active to show the active filters in the template
    origin_val = search_params.get('origin', '') or ''
    destination_val = search_params.get('destination', '') or ''
    date_val = search_params.get('date', '') or ''
    has_active_filters = bool((origin_val and origin_val.strip()) or 
                              (destination_val and destination_val.strip()) or 
                              (date_val and date_val.strip()))
    
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
    
    # Get flight object using the Flight from flights.py
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
            # For guests: validate form data only
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
        # For guests: empty form
        user_data = {
            'first_name': '',
            'last_name': '',
            'passport_number': '',
            'birth_date': '',
            'phone_numbers': ''
        }
    else:  # registered user
        # Get user data from database automatically filled
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
        # Final confirmation - process the order
        if user_type == 'guest':
            if not order.user_data:
                return redirect(f"/complete_booking/{flight_id}")

            order.email = user_email
            # Create order in DB (guest personal data NOT saved to DB)
            order_id, error = order.process_booking(order.flight, order.selected_seats)
        else:  # registered user
            # Get user object 
            user = users.read_user(user_email)
            # Create order in DB using existing user data from DB
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

@application.route("/manage_orders", methods=["GET", "POST"])
def manage_orders_for_guests():
    user_type = session.get('user_type')
    # Check if user is a manager
    if user_type == 'manager':
        return redirect("/?error=Managers cannot access the booking system. Please use the manager dashboard.")
    
    # Allow guests and users to access this page
    if not require_user_type(['user', 'guest']):
        return redirect("/?error=Please log in or continue as guest to manage orders")
    
    #Order management page for guests - requires order number
    if request.method == "POST":
        order_id = request.form.get("order_id", "").strip()
        if not order_id:
            return render_template("manage_orders.html", error="Please enter order number")
        
        order = Order.get_by_id(order_id)
        if not order:
            return render_template("manage_orders.html", error="Order not found")
        
        # Verify that the order belongs to the current user/guest
        user_email = session.get('user_email')
        if order.email != user_email:
            return render_template("manage_orders.html", error="You don't have access to this order")
        
        # Get display status
        status, _, final_price = order.get_display_status()
        
        # Calculate cancellation fee - use from status if cancelled, otherwise calculate for active orders
        if status == 'Cancelled by Customer':
            cancellation_fee = order.total_payment * 0.05
        elif status == 'Active':
            cancellation_fee = order.get_cancellation_fee()
        else:
            cancellation_fee = 0.0
        
        return render_template("order_details.html",
                             order=order,
                             display_status=status,
                             cancellation_fee=cancellation_fee,
                             final_price=final_price,
                             is_guest=True)
    
    return render_template("manage_orders.html")

@application.route("/my_orders")
def my_orders_for_users():
    #Order management page for registered users - shows all orders
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
    #View order details
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

@application.route("/cancel_order/<int:order_id>", methods=["GET", "POST"])
def cancel_order(order_id):
    #Handle order cancellation - GET shows confirmation page, POST cancels the order
    user_type = session.get('user_type')
    
    # Check if user is a manager
    if user_type == 'manager':
        return redirect("/?error=Managers cannot access the booking system. Please use the manager dashboard.")
    
    # Check if user is logged in as user or guest
    if not require_user_type(['user', 'guest']):
        return redirect("/?error=Please log in or continue as guest to cancel order")
    
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
    
    # POST request - actually cancel the order
    if request.method == "POST":
        success, error_message = order.cancel_by_customer()
        
        if not success:
            return render_template("error.html", error=error_message)
        
        # Redirect to orders page after successful cancellation
        is_guest = (user_type == 'guest')
        if is_guest:
            return redirect(f"/order_details/{order_id}?success=Order cancelled successfully")
        else:
            return redirect("/my_orders?success=Order cancelled successfully")
    
    # GET request - show confirmation page
    cancellation_fee = order.get_cancellation_fee()
    is_guest = (user_type == 'guest')
    
    return render_template("confirm_cancel.html",
                         order=order,
                         cancellation_fee=cancellation_fee,
                         is_guest=is_guest)


""" Manager routes """
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


#Select route before creating a flight
@application.route("/flights_management/select_route", methods=["GET", "POST"])
def select_route():
    #Step 1: Process route selection and move to step 2
    if not require_user_type(['manager']):
        return redirect("/manager?error=Access denied. Please log in as manager")
    
    # Handle GET request - redirect to flights_management
    if request.method == "GET":
        return redirect("/flights_management")
    
    # POST request - process form data
    origin_airport = request.form.get("origin_airport", "").strip()
    destination_airport = request.form.get("destination_airport", "").strip()
    departure_date = request.form.get("departure_date", "").strip()
    departure_time = request.form.get("departure_time", "").strip()
    
    if not all([origin_airport, destination_airport, departure_date, departure_time]):
        airports = get_all_airports()
        return render_template("flights_management.html", 
                             step=1,
                             airports=airports,
                             today=date.today().isoformat(),
                             error="Please fill all required fields")
    
    # Get route information
    route_info = get_flight_route_info(origin_airport, destination_airport)
    if not route_info:
        airports = get_all_airports()
        return render_template("flights_management.html", 
                             step=1,
                             airports=airports,
                             today=date.today().isoformat(),
                             error="Route not found in database")
    
    flight_duration, origin_country, destination_country = route_info #save the route information
    is_long = is_long_flight(flight_duration)
    
    # Calculate duration hours and minutes
    duration_hours = flight_duration // 60
    duration_minutes = flight_duration % 60
    
    route_info = {'duration_hours': duration_hours,'duration_minutes': duration_minutes,
        'is_long_flight': is_long} #save the route information to the dictionary
    
    # Get available planes (plane selection)
    available_planes = get_available_planes(origin_country, is_long_flight=is_long, 
                                          departure_date=departure_date, 
                                          departure_time=departure_time)
    
    # Get crew requirements for the next step 
    large_crew = get_crew_requirements('Large', is_long)
    small_crew = get_crew_requirements('Small', is_long)
    
    # Save route info and available planes to session for next steps
    session['flight_creation'] = {
        'origin_airport': origin_airport,
        'destination_airport': destination_airport,
        'departure_date': departure_date,
        'departure_time': departure_time,
        'route_info': route_info,
        'flight_duration': flight_duration,
        'origin_country': origin_country,
        'destination_country': destination_country,
        'is_long': is_long,
        'available_planes': available_planes
    }
    
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
                         available_pilots=[],
                         available_attendants=[],
                         today=date.today().isoformat())

#Select plane before selecting crew
@application.route("/flights_management/plane_selection", methods=["GET", "POST"])
def plane_selection():
    if not require_user_type(['manager']):
        return redirect("/manager?error=Access denied. Please log in as manager")
    
    # Handle GET request - redirect to flights_management
    if request.method == "GET":
        return redirect("/flights_management")
    
    # POST request - process form data
  
    flight_data = session.get('flight_creation')
    if not flight_data:
        return redirect("/flights_management")
    # Get route information from session 
    origin_airport = flight_data['origin_airport']
    destination_airport = flight_data['destination_airport']
    departure_date = flight_data['departure_date']
    departure_time = flight_data['departure_time']
    route_info = flight_data['route_info']
    origin_country = flight_data['origin_country']
    is_long = flight_data['is_long']

    plane_id = request.form.get("plane_id")
    
    # change the selected plane to the session if it's already selected
    if 'selected_plane_id' in flight_data:
        plane_id = flight_data['selected_plane_id']
    elif plane_id:
        # Save selected plane to session (first time selection)
        # Get plane size from available_planes
        try:
            plane_id_int = int(plane_id)
            selected_plane = next((p for p in available_planes if p[0] == plane_id_int), None)
            if selected_plane:
                flight_data['selected_plane_id'] = plane_id
                flight_data['selected_plane_size'] = selected_plane[2]  # Save plane size
                session['flight_creation'] = flight_data
        except (ValueError, TypeError):
            pass  # Invalid plane_id, will be handled later
    
    # Get previously selected crew (if any)
    selected_pilot_ids = request.form.getlist("pilot_ids")
    selected_attendant_ids = request.form.getlist("attendant_ids")
    price_economy = request.form.get("price_economy")
    price_business = request.form.get("price_business")
    
    # Get available planes from session (already fetched in step 1)
    available_planes = flight_data.get('available_planes', [])
    
    # Get crew requirements (to display requirements)
    large_crew = get_crew_requirements('Large', is_long)
    small_crew = get_crew_requirements('Small', is_long)
    
    # Get available pilots and attendants (needed in step 2 - crew selection)
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
                         selected_plane_id=plane_id,
                         plane_locked=('selected_plane_id' in flight_data),
                         selected_pilot_ids=selected_pilot_ids,
                         selected_attendant_ids=selected_attendant_ids,
                         price_economy=price_economy,
                         price_business=price_business,
                         large_crew=large_crew,
                         small_crew=small_crew,
                         available_pilots=available_pilots,
                         available_attendants=available_attendants,
                         pilot_error=None,
                         attendant_error=None,
                         crew_error=None,
                         today=date.today().isoformat())

@application.route("/flights_management/add_flight", methods=["POST"])
def add_flight_with_crew():
    if not require_user_type(['manager']):
        return redirect("/manager?error=Access denied. Please log in as manager")
    
    # Get route information from session 
    flight_data = session.get('flight_creation')
    if not flight_data:
        return redirect("/flights_management")
    
    origin_airport = flight_data['origin_airport']
    destination_airport = flight_data['destination_airport']
    departure_date = flight_data['departure_date']
    departure_time = flight_data['departure_time']
    origin_country = flight_data['origin_country']
    is_long = flight_data['is_long']
    route_info = flight_data['route_info']
    
    # Get plane_id and plane_size from session 
    plane_id = flight_data.get('selected_plane_id')
    plane_size = flight_data.get('selected_plane_size')
    
    if not plane_id or not plane_size:
        return redirect("/flights_management")
    
    try:
        plane_id_int = int(plane_id)
    except (ValueError, TypeError):
        return redirect("/flights_management")
    
    # Get form data
    price_economy = request.form.get("price_economy")
    price_business = request.form.get("price_business")
    
    # Get pilot and attendant IDs
    pilot_ids = request.form.getlist("pilot_ids")
    attendant_ids = request.form.getlist("attendant_ids")
    
    # Get available planes from session (already fetched in step 1)
    available_planes = flight_data.get('available_planes', [])
    
    # Get crew requirements (to display requirements)
    large_crew = get_crew_requirements('Large', is_long)
    small_crew = get_crew_requirements('Small', is_long)
    
    # Get crew requirements based on plane size
    crew_reqs = large_crew if plane_size == 'Large' else small_crew
    
    # Get available pilots and attendants needed for validation and error display
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
    
    # Validate crew selection
    pilot_error = None
    attendant_error = None
    crew_error = None
    
    #check if the number of pilots and attendants is correct
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
        # Clear session after successful flight creation
        session.pop('flight_creation', None)
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


@application.route("/manager/dashboard", methods=["GET", "POST"])
def manager_dashboard():
    #Manager dashboard - shows all flights with optional filtering
    if not require_user_type(['manager']):
        return redirect("/manager?error=Access denied. Please log in as manager")
    
    # Get filter parameters from request 
    filter_date = request.form.get("filter_date") or request.args.get("filter_date")
    filter_origin = request.form.get("filter_origin") or request.args.get("filter_origin")
    filter_destination = request.form.get("filter_destination") or request.args.get("filter_destination")
    filter_status = request.form.get("filter_status") or request.args.get("filter_status")
    
    # Get all airports for filter dropdowns
    airports = get_all_airports()
    
    # Get flights with filters
    flights = get_manager_flights(filter_date, filter_origin, filter_destination, filter_status)
    
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
    #Add a new plane to the fleet - two step process
    if not require_user_type(['manager']):
        return redirect("/manager?error=Access denied. Please log in as manager")
    
    # check if the plane is already created
    plane_data = session.get('plane_creation')
    is_step_2 = plane_data is not None
    
    if request.method == "POST":
        if not is_step_2:
            # Step 1: Plane basic details
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
            
            # Validate plane_id is an integer
            try:
                plane_id_int = int(plane_id)
            except ValueError:
                return render_template("add_plane.html",
                                     step=1,
                                     error="Please enter a plane ID that contains only numbers",
                                     plane_id=plane_id or "",
                                     manufacturer=manufacturer or "",
                                     size=size or "",
                                     purchase_date=purchase_date or "")
            
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
            
            # Save plane info to session for step 2
            session['plane_creation'] = {
                'plane_id': plane_id_int,
                'size': size,
                'manufacturer': manufacturer,
                'purchase_date': purchase_date
            }
            # Move to step 2 - seat configuration
            return render_template("add_plane.html",
                                 step=2,
                                 plane_id=plane_id_int,
                                 size=size,
                                 manufacturer=manufacturer,
                                 purchase_date=purchase_date)
        
        else:
            if not plane_data:
                return redirect("/manager/add_plane")
            
            plane_id_int = plane_data['plane_id']
            size = plane_data['size']
            manufacturer = plane_data['manufacturer']
            purchase_date = plane_data['purchase_date']
            
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
                    
                    # Insert plane into database (only after all seats are created)
                    data.sql_insert(
                        "INSERT INTO Planes (plane_id, manufacturer, size, purchase_date) VALUES (%s, %s, %s, %s)",
                        plane_id_int, manufacturer, size, purchase_date
                    )
                    
                    # Insert seats for Economy class
                    for row in range(1, economy_rows_int + 1):
                        for col in range(1, economy_seats_int + 1):
                            data.sql_insert(
                                "INSERT INTO Seats (plane_id, seat_row, seat_column, seat_class) VALUES (%s, %s, %s, %s)",
                                plane_id_int, row, col, 'Economy'
                            )
                    
                    # Clear session after successful creation
                    session.pop('plane_creation', None)
                    
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
                    
                    # Insert plane into database (only after all seats are created)
                    data.sql_insert(
                        "INSERT INTO Planes (plane_id, manufacturer, size, purchase_date) VALUES (%s, %s, %s, %s)",
                        plane_id_int, manufacturer, size, purchase_date
                    )
                    
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
                    
                    # Clear session after successful creation
                    session.pop('plane_creation', None)
                    
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
    
    # GET request - show form based on session
    if is_step_2:
        # Show step 2 form (seat configuration)
        return render_template("add_plane.html",
                             step=2,
                             plane_id=plane_data['plane_id'],
                             size=plane_data['size'],
                             manufacturer=plane_data['manufacturer'],
                             purchase_date=plane_data['purchase_date'])
    else:
        # Show step 1 form (plane basic details)
        return render_template("add_plane.html",
                             step=1,
                             plane_id="",
                             manufacturer="",
                             size="",
                             purchase_date="")

@application.route("/manager/reports")
def manager_reports():
    #Manager reports page - shows analytics and charts
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

@application.route("/manager/cancel_flight/<int:flight_id>", methods=["GET", "POST"])
def cancel_flight(flight_id):
    #Handle flight cancellation - GET shows confirmation page, POST cancels the flight
    if not require_user_type(['manager']):
        return redirect("/manager?error=Access denied. Please log in as manager")
    
    flight = Flight.get_flight_by_id(flight_id, include_all_statuses=True)
    if not flight:
        return render_template("error.html", error="Flight not found")
    
    # POST request - actually cancel the flight
    if request.method == "POST":
        if flight.status == 'Cancelled':
            return redirect("/manager/dashboard")
        
        # Cancel the flight
        success, error_msg = flight.cancel_flight()
        if not success:
            return render_template("error.html", error=error_msg)
        
        return redirect("/manager/dashboard")
    
    # GET request - show confirmation page
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

@application.route("/manager/confirm_cancel_flight/<int:flight_id>")
def confirm_cancel_flight(flight_id):
    """Redirect to cancel_flight for backward compatibility"""
    return redirect(f"/manager/cancel_flight/{flight_id}")

@application.route("/manager/add_employee", methods=["GET", "POST"])
def add_employee():
    """Add a new employee (Attendant or Pilot)"""
    if not require_user_type(['manager']):
        return redirect("/manager?error=Access denied. Please log in as manager")
    
    if request.method == "POST":
        employee_role = request.form.get("employee_role", "").strip()
        employee_id = request.form.get("employee_id", "").strip()
        first_name_he = request.form.get("first_name_he", "").strip()
        last_name_he = request.form.get("last_name_he", "").strip()
        phone_number = request.form.get("phone_number", "").strip()
        city = request.form.get("city", "").strip()
        street = request.form.get("street", "").strip()
        house_number = request.form.get("house_number", "").strip()
        start_work_date = request.form.get("start_work_date", "").strip()
        long_flight_certified = request.form.get("long_flight_certified", "").strip()
        
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
        
        # Validate employee ID
        is_valid, error = validations.validate_id_number(employee_id)
        if not is_valid:
            return render_template("add_employee.html",
                                 error=error,
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
        
        # Validate phone number
        is_valid, error = validations.validate_phone_number(phone_number)
        if not is_valid:
            return render_template("add_employee.html",
                                 error=error,
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
