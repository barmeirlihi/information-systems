#!/usr/bin/env python3
"""
WSGI entry point for AWS Elastic Beanstalk
This ensures the application can be found regardless of working directory
"""
import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Debug: Print current directory and files
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"Current directory: {current_dir}")
logger.info(f"Python path: {sys.path}")
logger.info(f"Files in directory: {os.listdir(current_dir) if os.path.exists(current_dir) else 'Directory not found'}")

try:
    # Check if application.py exists
    app_file = os.path.join(current_dir, 'application.py')
    if not os.path.exists(app_file):
        raise FileNotFoundError(f"application.py not found at {app_file}")
    
    logger.info(f"Found application.py at {app_file}")
    
    # Import the application
    import importlib.util
    spec = importlib.util.spec_from_file_location("application", app_file)
    if spec is None:
        raise ImportError(f"Could not create spec for application.py")
    
    app_module = importlib.util.module_from_spec(spec)
    sys.modules['application'] = app_module
    spec.loader.exec_module(app_module)
    
    application = app_module.application
    logger.info("Successfully imported application")
except Exception as e:
    logger.error(f"Failed to import application: {e}", exc_info=True)
    raise

# This is what gunicorn will use
__all__ = ['application']

