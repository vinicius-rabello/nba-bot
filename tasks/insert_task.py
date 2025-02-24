import sys
from pathlib import Path

# Add the root directory to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))
sys.path.append("/opt/airflow/database")

# database/insert_task.py
from database.db_connection import Database

def insert_nba_games(**context):
    """Task to insert the nba games df into PostgreSQL."""
    # Pull the DataFrame from XCom
    ti = context['ti']
    df = ti.xcom_pull(task_ids='scraping_task')
    db = Database()
    db.insert_or_update_nba_games(df)  # Insert/update into DB
    db.close()