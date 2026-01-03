import pandas as pd
import mysql.connector
from contextlib import contextmanager
from mysql.connector import cursor

import data
from data import *
email = 'reg1@gmail.com'


class User:
    def __init__(self, email, password, first_name, last_name, phone_numbers, registration_date, birth_date,
                 passport_number):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = first_name + " " + last_name
        self.phone_numbers = phone_numbers
        self.registration_date = registration_date
        self.birth_date = birth_date
        self.passport_number = passport_number

    def __str__(self):
        return (f"User: {self.full_name}\n"
                f"Email: {self.email}\n"
                f"Passport: {self.passport_number}\n"
                f"Birth Date: {self.birth_date}\n"
                f"Phones: {self.phone_numbers}")


def read_user(email):
    # שליפה מהדאטה בייס
    result = data.sql_query("""SELECT u.email, r.password, u.first_name, u.last_name, 
                                      r.passport_number, r.birth_date, r.registration_date
                               FROM Users as u
                               JOIN RegisteredUsers as r ON r.email = u.email
                               WHERE u.email = %s""", email)

    if not result:
        return None

    user_data = result[0]

    # שליפת טלפונים
    phones_raw = data.sql_query("SELECT phone_number FROM UserPhones WHERE email = %s", email)
    phone_numbers = [p[0] for p in phones_raw]

    # יצירת האובייקט
    new_user = User(
        email=user_data[0],
        password=user_data[1],
        first_name=user_data[2],
        last_name=user_data[3],
        phone_numbers=phone_numbers,
        passport_number=user_data[4],  # הנה הדרכון
        birth_date=user_data[5],
        registration_date=user_data[6]
    )

    return new_user


# --- בדיקה ---
user1 = read_user('reg1@gmail.com')
print(user1)


def get_password():
    return data.sql_query("""SELECT u.password from Users WHERE email = %s""", email)

