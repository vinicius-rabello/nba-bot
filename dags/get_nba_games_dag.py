import datetime

import sys
sys.path.append("/opt/airflow/scrapers")

from scrapers.scraper_task import scrape_nba_task


from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "viniciusrabello",
    "retries": 5,
    "retry_delay": datetime.timedelta(minutes=5)
}

with DAG (
    default_args=default_args,
    dag_id="nba_games_dag_v01",
    description="This DAG scrapes the NBA games happening at execution date.",
    start_date=datetime.datetime(2025, 2, 18),
    schedule_interval="@daily"
) as dag:
    task1 = PythonOperator(
        task_id = "scraping_task",
        python_callable=scrape_nba_task('2025-02-19')
    )

    task1