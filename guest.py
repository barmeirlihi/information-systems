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
    
    def get_booking_form_data(self):
        """Returns guest data for booking form (empty fields for new data)"""
        return {
            'first_name': self.first_name if self.first_name else '',
            'last_name': self.last_name if self.last_name else '',
            'passport_number': '',
            'birth_date': '',
            'phone_numbers': ', '.join(self.phone_numbers) if self.phone_numbers else ''
        }
    
    def validate_booking_data(self, form_data):
        """
        Validates guest booking form data
        Returns: (is_valid, error_message, validated_data)
        """
        first_name = form_data.get("first_name", "").strip()
        last_name = form_data.get("last_name", "").strip()
        passport_number = form_data.get("passport_number", "").strip()
        birth_date = form_data.get("birth_date", "").strip()
        phone_numbers = form_data.get("phone_numbers", "").strip()
        
        if not all([first_name, last_name, passport_number, birth_date, phone_numbers]):
            return False, "Please fill in all required fields", None
        
        validated_data = {
            'first_name': first_name,
            'last_name': last_name,
            'passport_number': passport_number,
            'birth_date': birth_date,
            'phone_numbers': phone_numbers
        }
        
        return True, None, validated_data
    
    def add_order(self, order, form_data):
        """
        Creates an order for a guest
        Validates form data and creates order in database
        IMPORTANT: Guest personal data (name, passport, etc.) is NOT saved to DB - only the order is saved
        
        Args:
            order: Order object
            form_data: Form data dictionary (from form, not from DB)
            
        Returns: (order_id, error_message)
        """
        # Validate form data (no DB check - just format validation)
        is_valid, error, validated_data = self.validate_booking_data(form_data)
        if not is_valid:
            return None, error
        
        # Set guest data in order (from form, NOT saved to DB - only used for order confirmation)
        order.user_data = validated_data
        order.email = self.email
        
        # Create order in database (only order is saved, guest personal data is NOT saved to DB)
        order_id, error = order.process_booking(order.flight, order.selected_seats)
        
        return order_id, error

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
