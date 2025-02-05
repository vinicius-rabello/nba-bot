# config/db_config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection string (PostgreSQL)
DB_URI = os.getenv("DB_URI")