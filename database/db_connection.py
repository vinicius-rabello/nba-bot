import psycopg2
import sys
from pathlib import Path

# Add the root directory to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))
sys.path.append("/opt/airflow/config")

from config.db_config import DB_URI
import pandas as pd


class Database:
    """Database connection class for handling PostgreSQL operations."""

    def __init__(self):
        """Initialize the database connection."""
        self.conn = psycopg2.connect(DB_URI)
        self.cursor = self.conn.cursor()

    def insert_or_update_nba_games(self, df):
        """Insert or update NBA games in the database."""
        for _, row in df.iterrows():
            row = row.where(pd.notna(row), None)  # Convert NaN to None

            self.cursor.execute("""
                INSERT INTO games (game_id, date, time, broadcaster, home_team, away_team, home_team_score, away_team_score, arena, city, state)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (game_id) DO UPDATE SET 
                    home_team_score = COALESCE(EXCLUDED.home_team_score, games.home_team_score),
                    away_team_score = COALESCE(EXCLUDED.away_team_score, games.away_team_score);
            """, (
                row['game_id'], row['date'], row['time'], row['broadcaster'],
                row['home_team'], row['away_team'],
                None if row['home_team_score'] is None else int(
                    row['home_team_score']),
                None if row['away_team_score'] is None else int(
                    row['away_team_score']),
                row['arena'], row['city'], row['state']
            ))

        self.conn.commit()

    def get_games(self):
        """Read games table."""
        self.cursor.execute("""
            SELECT * FROM games;
        """)
        data=self.cursor.fetchall()
        return data


    def close(self):
        """Close the database connection."""
        self.cursor.close()
        self.conn.close()
