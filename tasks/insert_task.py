import sys
from pathlib import Path

# Add the root directory to sys.path
root_dir = Path(__file__).resolve().parent.parent  # Go up two levels to the root directory
sys.path.append(str(root_dir))

# database/insert_task.py
from database.db_connection import Database

def insert_nba_games(df):
    """Task to insert the nba games df into PostgreSQL."""
    db = Database()
    db.insert_or_update_nba_games(df)  # Insert/update into DB
    db.close()