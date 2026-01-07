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


app = Flask(__name__)
app.config.update(
    SESSION_TYPE="filesystem",
    SESSION_FILE_DIR="./flask_session_data",
    SESSION_PERMANENT=True,
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=10),
    SESSION_REFRESH_EACH_REQUEST=True,
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
        # Handle seat booking
        selected_seats = request.form.getlist('selected_seats')
        if not selected_seats:
            return render_template("select_seats.html", 
                                 flight=flight_tuple,
                                 seats_by_row=seats_by_row,
                                 price_economy=flight.price_economy,
                                 price_business=flight.price_business,
                                 error="Please select at least one seat")
        
        # Process booking using Order class
        user_email = session.get('user_email')
        order = Order(email=user_email)
        order_id, error = order.process_booking(flight, selected_seats)
        
        if error:
            return render_template("select_seats.html", 
                                 flight=flight_tuple,
                                 seats_by_row=seats_by_row,
                                 price_economy=flight.price_economy,
                                 price_business=flight.price_business,
                                 error=error)
        
        # Success - refresh seats to show updated availability
        seats_by_row = flight.organize_seats_by_row()
        return render_template("select_seats.html", 
                             flight=flight_tuple,
                             seats_by_row=seats_by_row,
                             price_economy=flight.price_economy,
                             price_business=flight.price_business,
                             success=f"Successfully booked {len(selected_seats)} seat(s)! Order ID: {order_id}")
    
    return render_template("select_seats.html", 
                         flight=flight_tuple,
                         seats_by_row=seats_by_row,
                         price_economy=flight.price_economy,
                         price_business=flight.price_business)

@app.route("/flights_management")
def flights_management():
    if not require_user_type(['manager']):
        return render_template("manager.html", message='Access denied. Please log in as a manager.')
    return render_template("flights_management.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
