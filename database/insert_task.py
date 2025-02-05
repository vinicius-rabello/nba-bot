# database/insert_task.py
from database.db_connection import Database

def insert_games(df):
    """Task to insert a dataframe into PostgreSQL."""
    db = Database()
    db.insert_or_update_games(df)  # Insert/update into DB
    db.close()