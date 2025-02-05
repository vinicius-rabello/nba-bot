# database/db_connection.py
import psycopg2
from config.db_config import DB_URI

class Database:
    """Database connection class for handling PostgreSQL operations."""
    
    def __init__(self):
        """Initialize the database connection."""
        self.conn = psycopg2.connect(DB_URI)
        self.cursor = self.conn.cursor()

    def insert_or_update_games(self, df):
        """Insert or update NBA games in the database."""
        for _, row in df.iterrows():
            self.cursor.execute("""
                INSERT INTO nba_games (game_id, date, time, broadcaster, home_team, away_team, arena, city, state)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (game_id) DO UPDATE SET 
                    time = EXCLUDED.time,
                    broadcaster = EXCLUDED.broadcaster;
            """, tuple(row))

        self.conn.commit()

    def close(self):
        """Close the database connection."""
        self.cursor.close()
        self.conn.close()
