"""
Validation functions for form inputs
All functions return (is_valid: bool, error_message: str or None)
"""

import re
from datetime import datetime


def validate_email(email):
    """
    Validates email format - must contain @ symbol
    
    Args:
        email: Email string to validate
        
    Returns:
        (is_valid: bool, error_message: str or None)
    """
    if not email or not isinstance(email, str):
        return False, "Email is required"
    
    email = email.strip()
    
    if not email:
        return False, "Email cannot be empty"
    
    if '@' not in email:
        return False, "Email must contain @ symbol"
    
    # Additional basic validation - email should have format like user@domain
    parts = email.split('@')
    if len(parts) != 2:
        return False, "Invalid email format"
    
    if not parts[0] or not parts[1]:
        return False, "Email must have both username and domain"
    
    if '.' not in parts[1]:
        return False, "Email domain must contain a dot"
    
    return True, None


def validate_phone_number(phone_string):
    """
    Validates phone number(s) - after splitting by comma, each item should be only numbers or with dash
    
    Args:
        phone_string: Phone number string (can contain multiple numbers separated by commas)
        
    Returns:
        (is_valid: bool, error_message: str or None)
    """
    if not phone_string or not isinstance(phone_string, str):
        return False, "Phone number is required"
    
    phone_string = phone_string.strip()
    
    if not phone_string:
        return False, "Phone number cannot be empty"
    
    # Split by comma
    phone_numbers = [phone.strip() for phone in phone_string.split(',')]
    
    # Remove empty strings
    phone_numbers = [phone for phone in phone_numbers if phone]
    
    if not phone_numbers:
        return False, "At least one phone number is required"
    
    # Validate each phone number
    for phone in phone_numbers:
        # Remove all dashes for validation
        phone_without_dash = phone.replace('-', '')
        
        # Check if remaining characters are only digits
        if not phone_without_dash.isdigit():
            return False, f"Phone number '{phone}' contains invalid characters. Only numbers and dashes are allowed"
        
        # Check if phone number is not empty after removing dashes
        if not phone_without_dash:
            return False, f"Phone number '{phone}' is invalid"
    
    return True, None


def validate_passport_number(passport_number):
    """
    Validates passport number - must be only digits
    
    Args:
        passport_number: Passport number string to validate
        
    Returns:
        (is_valid: bool, error_message: str or None)
    """
    if not passport_number or not isinstance(passport_number, str):
        return False, "Passport number is required"
    
    passport_number = passport_number.strip()
    
    if not passport_number:
        return False, "Passport number cannot be empty"
    
    if not passport_number.isdigit():
        return False, "Passport number must contain only digits"
    
    return True, None


def validate_id_number(id_number):
    """
    Validates ID number - must be only digits
    
    Args:
        id_number: ID number string to validate
        
    Returns:
        (is_valid: bool, error_message: str or None)
    """
    if not id_number or not isinstance(id_number, str):
        return False, "ID number is required"
    
    id_number = id_number.strip()
    
    if not id_number:
        return False, "ID number cannot be empty"
    
    if not id_number.isdigit():
        return False, "ID number must contain only digits"
    
    return True, None


def validate_name(name, field_name="Name"):
    """
    Validates name - should not be empty and should contain only letters, spaces, and hyphens
    
    Args:
        name: Name string to validate
        field_name: Name of the field for error messages (e.g., "First Name", "Last Name")
        
    Returns:
        (is_valid: bool, error_message: str or None)
    """
    if not name or not isinstance(name, str):
        return False, f"{field_name} is required"
    
    name = name.strip()
    
    if not name:
        return False, f"{field_name} cannot be empty"
    
    # Check if name contains only letters, spaces, hyphens, and apostrophes
    if not re.match(r"^[a-zA-Z\s\-']+$", name):
        return False, f"{field_name} can only contain letters, spaces, hyphens, and apostrophes"
    
    return True, None


def validate_date(date_string, field_name="Date"):
    """
    Validates date format - should be in YYYY-MM-DD format
    
    Args:
        date_string: Date string to validate
        field_name: Name of the field for error messages
        
    Returns:
        (is_valid: bool, error_message: str or None)
    """
    if not date_string or not isinstance(date_string, str):
        return False, f"{field_name} is required"
    
    date_string = date_string.strip()
    
    if not date_string:
        return False, f"{field_name} cannot be empty"
    
    try:
        # Try to parse the date
        datetime.strptime(date_string, '%Y-%m-%d')
        return True, None
    except ValueError:
        return False, f"{field_name} must be in YYYY-MM-DD format"


def validate_password(password):
    """
    Validates password - should not be empty and should have minimum length
    
    Args:
        password: Password string to validate
        
    Returns:
        (is_valid: bool, error_message: str or None)
    """
    if not password or not isinstance(password, str):
        return False, "Password is required"
    
    password = password.strip()
    
    if not password:
        return False, "Password cannot be empty"
    
    if len(password) < 4:
        return False, "Password must be at least 4 characters long"
    
    return True, None

