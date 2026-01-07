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
                               JOIN guests as g ON g.UserEmail = u.email
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
    guest_obj = read_guest(email)
    return guest_obj is not None

def add_guest(guest):
    if is_guest(guest.email):
        return False

    # בדיקה אם המשתמש כבר קיים ב-Users
    existing_user = data.sql_query("SELECT email FROM Users WHERE email = %s", guest.email)
    if not existing_user:
        # רק אם המשתמש לא קיים - ניצור אותו
        data.sql_insert("INSERT INTO Users (email, first_name, last_name) VALUES (%s, %s, %s)",
                                guest.email, guest.first_name, guest.last_name)
    else:
        # אם המשתמש כבר קיים - נעדכן את הפרטים שלו
        data.sql_insert("UPDATE Users SET first_name = %s, last_name = %s WHERE email = %s",
                                guest.first_name, guest.last_name, guest.email)

    # 2. יצירת Guest (אם הוא לא קיים כבר)
    data.sql_insert("""INSERT IGNORE INTO Guests (UserEmail)
                               VALUES (%s)""",
                            guest.email)

    if guest.phone_numbers:
        # phone_numbers is already a list
        if isinstance(guest.phone_numbers, str):
            phones_list = guest.phone_numbers.split(',')
        else:
            phones_list = guest.phone_numbers
        query_phone = "INSERT INTO UserPhones (email, phone_number) VALUES (%s, %s)"
        for phone in phones_list:
            clean_phone = phone.strip() if isinstance(phone, str) else str(phone).strip()  # מנקה רווחים מיותרים בצדדים
            if clean_phone:  # מוודא שלא מכניסים סתם ריק
                data.sql_insert(query_phone, guest.email, clean_phone)
