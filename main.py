from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from datetime import timedelta

import data
import users
from data import *
from users import *
from flights import *


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
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")  # unique value
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        phone_numbers = request.form.getlist("phone_numbers", ",")
        birth_date = request.form.get("birth_date")
        passport_number = request.form.get("passport_number")
        query = """
            INSERT INTO RegisteredUsers (password, email, last_name, first_name, passport_number, birth_date, registration_date)
            VALUES (%s, %s, %s, %s, %s, %s, CURDATE())
        """
        data.sql_insert(query, password, email, first_name, last_name, phone_numbers, birth_date, passport_number)

        return render_template("sign_up.html")

        if users.get_password(email) == password:
            return redirect("/book_flights.html")
        else:
            return render_template("login.html", message='Incorrect Login Details.')
    return render_template("login.html")

@app.route("/guest", methods=["POST", "GET"])
def guest():
    if request.method == "POST":
        email = request.form.get("email")  # unique value
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        return redirect("/book_flights.html")

    return render_template("guest.html")

@app.route("/gabi-guest-3", methods=["POST", "GET"])
def guest():
    if request.method == "POST":
        email = request.form.get("email")  # unique value
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        return redirect("/book_flights.html")

    return render_template("gabi-guest.html")

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
    app.run(debug=True)
