# config/db_config.py
import os
import logging
from dotenv import load_dotenv

# Specify the exact path to the .env file
env_path = "/opt/airflow/.env"
logging.info(f"Looking for .env file at: {env_path}")
load_dotenv(dotenv_path=env_path)

# Log for debugging
DB_URI = os.getenv("DB_URI")
logging.info(f"DB_URI after loading: {DB_URI}")

if not DB_URI:
    logging.error("DB_URI is not set! Check your .env file and permissions.")