import pandas as pd
import mysql.connector
from contextlib import contextmanager
from mysql.connector import cursor

import data
from data import *

class Guest:
    def __init__(self, email, first_name, last_name, phone_numbers):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = first_name + " " + last_name
        self.phone_numbers = phone_numbers

def read_guest(email):
    # שליפה מהדאטה בייס
    result = data.sql_query("""SELECT u.email, u.first_name, u.last_name
                               FROM Users as u
                               JOIN guests as g ON g.email = u.email
                               WHERE u.email = %s""", email)

    if not result:
        return None

    user_data = result[0]

    phones_raw = data.sql_query("SELECT phone_number FROM UserPhones WHERE email = %s", email)
    phone_numbers = [p[0] for p in phones_raw]

    # יצירת האובייקט
    new_guest = Guest(
        email=user_data[0],
        first_name=user_data[1],
        last_name=user_data[2],
        phone_numbers=phone_numbers
    )

    return new_guest

def is_guest(email):
    result = data.sql_query("""select * from guests where UserEmail = %s""", email)
    if not result:
        return False
    return read_guest(email)

def add_guest(guest):
    if is_guest(guest.email):
        return False

    data.sql_insert("INSERT INTO Users (email, first_name, last_name) VALUES (%s, %s, %s)",
                            guest.email, guest.first_name, guest.last_name)

            # 2. יצירת RegisteredUser
    data.sql_insert("""INSERT INTO Guests (UserEmail)
                               VALUES (%s)""",
                            guest.email)

    if guest.phone_numbers:
        phones_list = guest.phone_numbers.split(',')
        query_phone = "INSERT INTO UserPhones (email, phone_number) VALUES (%s, %s)"
        for phone in phones_list:
            clean_phone = phone.strip()  # מנקה רווחים מיותרים בצדדים
            if clean_phone:  # מוודא שלא מכניסים סתם ריק
                data.sql_insert(query_phone, guest.email, clean_phone)
