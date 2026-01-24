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
    
    def get_booking_form_data(self):
        """Returns user data for booking form (read-only for registered users)"""
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'passport_number': self.passport_number,
            'birth_date': str(self.birth_date),
            'phone_numbers': ', '.join(self.phone_numbers) if self.phone_numbers else ''
        }
    
    def add_order(self, order):
        """
        Creates an order for a registered user
        Uses existing user data from database
        Updates order with user data and creates order in DB
        
        Args:
            order: Order object
            
        Returns: (order_id, error_message)
        """
        # Set user data in order (from database)
        order.user_data = self.get_booking_form_data()
        order.email = self.email
        
        # Create order in database (saves for both users and guests)
        order_id, error = order.process_booking(order.flight, order.selected_seats)
        
        return order_id, error


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


def get_password(email):
    result = data.sql_query("""SELECT r.password from RegisteredUsers as r WHERE email = %s""", email)
    if not result:
        return None
    return result[0][0]


def is_user(email):
    """Check if email exists in Users table (both guests and registered users)"""
    try:
        result = data.sql_query("""SELECT * FROM Users WHERE email = %s""", email)
        if not result:
            return False
        return True
    except Exception as e:
        print(f"Error checking if user exists: {e}")
        return False

def is_registered_user(email):
    """Check if email is a registered user (in RegisteredUsers table)"""
    try:
        result = data.sql_query("""SELECT * FROM RegisteredUsers WHERE email = %s""", email)
        if not result:
            return False
        return True
    except Exception as e:
        print(f"Error checking if registered user exists: {e}")
        return False

def add_user(user):
    if is_user(user.email):
        return False

    data.sql_insert("INSERT INTO Users (email, first_name, last_name) VALUES (%s, %s, %s)",
                            user.email, user.first_name, user.last_name)

            # 2. יצירת RegisteredUser
    data.sql_insert("""INSERT INTO RegisteredUsers (email, password, passport_number, birth_date, registration_date)
                               VALUES (%s, %s, %s, %s, CURDATE())""",
                            user.email, user.password, user.passport_number, user.birth_date)

    if user.phone_numbers:
        phones_list = user.phone_numbers.split(',')
        query_phone = "INSERT INTO UserPhones (email, phone_number) VALUES (%s, %s)"
        for phone in phones_list:
            clean_phone = phone.strip()  # מנקה רווחים מיותרים בצדדים
            if clean_phone:  # מוודא שלא מכניסים סתם ריק
                data.sql_insert(query_phone, user.email, clean_phone)


if __name__ == "__main__":
    print(get_password('lihibarmeir@mail.tau.ac.il'))
