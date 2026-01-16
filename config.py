"""
Configuration settings for HouseMate application.
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Database
DATABASE_PATH = BASE_DIR / 'database' / 'housemate.db'

# Flask
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Upload settings
UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

# Session
SESSION_TYPE = 'filesystem'

# CSRF Protection
WTF_CSRF_ENABLED = True
WTF_CSRF_TIME_LIMIT = None  # No time limit for CSRF tokens

# Content Security Policy
CSP_ENABLED = True
CSP_DIRECTIVES = {
    'default-src': ["'self'"],
    'script-src': ["'self'", 'cdn.jsdelivr.net'],
    'style-src': ["'self'", "'unsafe-inline'", 'cdn.jsdelivr.net'],
    'img-src': ["'self'", 'data:', 'https:'],
    'font-src': ["'self'", 'cdn.jsdelivr.net'],
    'connect-src': ["'self'"],
    'frame-ancestors': ["'none'"],
    'base-uri': ["'self'"],
    'form-action': ["'self'"],
}

# CORS Configuration (Cross-Origin Resource Sharing)
# By default, CORS is restricted - only same-origin requests allowed
CORS_ENABLED = True
CORS_CONFIG = {
    'origins': [
        'http://localhost:5000',
        'http://127.0.0.1:5000',
        'http://localhost:3000',  # For frontend development if separate
    ],
    'methods': ['GET', 'POST', 'OPTIONS'],
    'allow_headers': ['Content-Type', 'Authorization', 'X-CSRF-Token'],
    'supports_credentials': True,
    'max_age': 3600,  # 1 hour
    'send_wildcard': False,  # Do NOT use wildcard '*'
}

# Application
APP_NAME = 'HouseMate'
VERSION = '1.0.0'
