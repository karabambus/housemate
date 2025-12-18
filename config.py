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

# Application
APP_NAME = 'HouseMate'
VERSION = '1.0.0'
