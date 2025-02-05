# database/insert_task.py
from database.db_connection import Database

def insert_nba_games(df):
    """Task to insert the nba games df into PostgreSQL."""
    db = Database()
    db.insert_or_update_nba_games(df)  # Insert/update into DB
    db.close()