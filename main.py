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


flytau_db = {"Donald@mail.tau.ac.il": "123!@ABC"}

@app.route("/")
def homepage():
    return render_template('homepage.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")  # unique value
        password = request.form.get("password")
        if users.get_password(email) == password:
            return redirect("/book_flights.html")
        else:
            return render_template("login.html", message='Incorrect Login Details.')
    return render_template("login.html")

@app.route("/sign_up", methods=["POST", "GET"])
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

        new_user = User(email, password, first_name, last_name, birth_date, passport_number, phones_string)
        try:
            add_user(new_user)
            return redirect("/book_flights")

        except Exception as e:
            print(f"Error: {e}")
            return render_template("sign_up.html", message="Error registering user")

    return render_template("sign_up.html")


@app.route("/guest", methods=["POST", "GET"])
def guest_page():
    if request.method == "POST":
        email = request.form.get("email")

        # 1. בדיקה האם הוא כבר קיים כאורח
        if guest.is_guest(email):
            return redirect("/book_flights.html")

        # 2. בדיקה חדשה: האם הוא קיים כמשתמש רשום?
        # (אנחנו יודעים שהוא לא אורח כי עברנו את ה-if הראשון)
        elif users.is_user(email):
            # אם הוא משתמש רשום, נזרוק אותו לדף לוגין עם הודעה מתאימה
            return render_template("login.html", message="You are a registered user. Please log in.")

        # 3. אם הוא לא אורח ולא רשום -> הוא משתמש חדש לגמרי
        else:
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            phone = request.form.get("phone")

            # אם שלחו לנו את הפרטים (שלב ב') -> ניצור את האורח
            if first_name and last_name and phone:
                # יצירת אובייקט אורח ושליחה לפונקציה (העברת הטלפון כרשימה)
                new_guest = Guest(email, first_name, last_name, [phone])
                guest.add_guest(new_guest)
                return redirect("/book_flights.html")

            # אם אין פרטים (שלב א') -> נטען את הדף עם השדות הפתוחים
            return render_template("guest.html", show_details=True, email_value=email)

    return render_template("guest.html")

@app.route("/manager", methods=["POST", "GET"])
def manager():
    if request.method == "POST":
        manager_id = request.form.get("manager_id")  # unique value
        password = request.form.get("password")
        if data.sql_query("""select password from Managers where manager_id = %s""", manager_id) == password:
            return redirect("/flights_management.html")
        else:
            return render_template("manager.html", message='Incorrect Login Details.')
    return render_template("manager.html")



if __name__ == "__main__":
    app.run(debug=True, port=5001)
