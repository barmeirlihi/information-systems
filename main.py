from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from datetime import timedelta

import data
import guest
import users
from data import *
from users import *
from flights import *
from guest import *
from order import Order


app = Flask(__name__)
app.config.update(
    SESSION_TYPE="filesystem",
    SESSION_FILE_DIR="./flask_session_data",
    SESSION_PERMANENT=True,
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=10),
    SESSION_REFRESH_EACH_REQUEST=False,
    SESSION_FILE_THRESHOLD=20,
    SESSION_COOKIE_SECURE=True
)
Session(app)

flytau_db = {"Donald@mail.tau.ac.il": "123!@ABC"}


def require_user_type(allowed_types):
    """בודק אם המשתמש מחובר וסוג המשתמש מורשה"""
    user_type = session.get('user_type')
    if not user_type or user_type not in allowed_types:
        return False
    return True

@app.route("/")
def homepage():
    return render_template('homepage.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        stored_password = users.get_password(email)
        if stored_password and stored_password == password:
            session['user_type'] = 'user'
            session['user_email'] = email
            return redirect("/book_flights")
        else:
            return render_template("login.html", message='Incorrect Login Details.')
    return render_template("login.html")

@app.route("/sign_up", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        # קליטת נתונים
        email = request.form.get("email")
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        birth_date = request.form.get("birth_date")
        passport_number = request.form.get("passport_number")

        # קליטת מחרוזת הטלפונים (למשל: "050-123, 052-456")
        phones_string = request.form.get("phone_numbers")

        new_user = User(email, password, first_name, last_name, phones_string, None, birth_date, passport_number)
        try:
            add_user(new_user)
            session['user_type'] = 'user'
            session['user_email'] = email
            return redirect("/book_flights")

        except Exception as e:
            print(f"Error: {e}")
            return render_template("sign_up.html", message="Error registering user")

    return render_template("sign_up.html")


@app.route("/guest", methods=["POST", "GET"])
def guest_page():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        phone = request.form.get("phone")

        # שלב א': אם יש רק email -> נבדוק מה הסטטוס שלו
        if email and not (first_name and last_name and phone):
            # 1. בדיקה האם הוא כבר קיים כאורח
            if guest.is_guest(email):
                session['user_type'] = 'guest'
                session['user_email'] = email
                return redirect("/book_flights")
            
            # 2. בדיקה האם הוא קיים כמשתמש רשום
            elif users.is_user(email):
                return render_template("login.html", message="You are a registered user. Please log in.")
            
            # 3. אם הוא לא אורח ולא רשום -> נטען את הדף עם השדות הפתוחים
            else:
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

    return render_template("guest.html")

@app.route("/manager", methods=["POST", "GET"])
def manager():
    if request.method == "POST":
        manager_id = request.form.get("manager_id")
        password = request.form.get("password")
        result = data.sql_query("""SELECT password FROM Managers WHERE manager_id = %s""", manager_id)
        if result and len(result) > 0 and result[0][0] == password:
            session['user_type'] = 'manager'
            session['manager_id'] = manager_id
            return redirect("/flights_management")
        else:
            return render_template("manager.html", message='Incorrect Login Details.')
    return render_template("manager.html")

@app.route("/book_flights", methods=["GET", "POST"])
def book_flights():
    if not require_user_type(['user', 'guest']):
        return redirect("/")
    
    airports = get_all_airports()
    flight_objects = []
    search_params = {}
    
    if request.method == "POST":
        origin = request.form.get("origin")
        destination = request.form.get("destination")
        date = request.form.get("date")
        
        search_params = {
            'origin': origin,
            'destination': destination,
            'date': date
        }
        
        flight_objects = Flight.get_active_flights(origin=origin if origin else None, 
                                                    destination=destination if destination else None,
                                                    flight_date=date if date else None)
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
    
    return render_template("book_flights.html", 
                         airports=airports, 
                         flights=flights_with_images,
                         search_params=search_params)

@app.route("/select_seats/<int:flight_id>", methods=["GET", "POST"])
def select_seats(flight_id):
    if not require_user_type(['user', 'guest']):
        return redirect("/")
    
    # Get flight object using the Flight class
    flight = Flight.get_flight_by_id(flight_id)
    if not flight:
        return redirect("/book_flights")
    
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

@app.route("/complete_booking/<int:flight_id>", methods=["GET", "POST"])
def complete_booking(flight_id):
    if not require_user_type(['user', 'guest']):
        return redirect("/")
    
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

@app.route("/confirm_booking/<int:flight_id>", methods=["GET", "POST"])
def confirm_booking(flight_id):
    if not require_user_type(['user', 'guest']):
        return redirect("/")
    
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

@app.route("/flights_management")
def flights_management():
    if not require_user_type(['manager']):
        return render_template("manager.html", message='Access denied. Please log in as a manager.')
    return render_template("flights_management.html")

@app.route("/manage_orders", methods=["GET", "POST"])
def manage_orders():
    """Order management page for guests - requires order number"""
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
        
        # Get display status
        status, cancellation_fee, final_price = order.get_display_status()
        
        return render_template("order_details.html",
                             order=order,
                             display_status=status,
                             cancellation_fee=cancellation_fee,
                             final_price=final_price,
                             is_guest=True)
    
    return render_template("manage_orders.html")

@app.route("/my_orders")
def my_orders():
    """Order management page for registered users - shows all orders"""
    if not require_user_type(['user']):
        return redirect("/login")
    
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

@app.route("/order_details/<int:order_id>")
def order_details(order_id):
    """View order details"""
    user_type = session.get('user_type')
    
    if user_type not in ['user', 'guest']:
        return redirect("/")
    
    order = Order.get_by_id(order_id)
    if not order:
        return render_template("error.html", error="Order not found")
    
    # Get display status
    status, _, final_price = order.get_display_status()
    
    # Calculate cancellation fee - use from status if cancelled, otherwise calculate for active orders
    if status == 'Cancelled by Customer':
        cancellation_fee = order.total_payment * 0.05
    elif status == 'Active':
        cancellation_fee = order.get_cancellation_fee()
    else:
        cancellation_fee = 0.0
    
    is_guest = (user_type == 'guest' or user_type is None)
    
    return render_template("order_details.html",
                         order=order,
                         display_status=status,
                         cancellation_fee=cancellation_fee,
                         final_price=final_price,
                         is_guest=is_guest)

@app.route("/confirm_cancel/<int:order_id>")
def confirm_cancel(order_id):
    """Confirmation page before cancelling an order"""
    user_type = session.get('user_type')
    
    if user_type not in ['user', 'guest']:
        return redirect("/")
    
    order = Order.get_by_id(order_id)
    if not order:
        return render_template("error.html", error="Order not found")
    
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

@app.route("/cancel_order/<int:order_id>", methods=["POST"])
def cancel_order(order_id):
    """Cancel an order"""
    user_type = session.get('user_type')
    
    if user_type not in ['user', 'guest']:
        return redirect("/")
    
    order = Order.get_by_id(order_id)
    if not order:
        return render_template("error.html", error="Order not found")
    
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
                             order=order,
                             display_status=status,
                             cancellation_fee=cancellation_fee,
                             final_price=final_price,
                             is_guest=True,
                             cancelled=True)
    else:
        return redirect("/my_orders")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
