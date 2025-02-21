import datetime

import sys
sys.path.append("/opt/airflow/tasks")

from tasks.scraper_task import scrape_nba_task
# from tasks.insert_task import insert_nba_games


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
    start_date=datetime.datetime(2025, 2, 20),
    schedule_interval="@daily"
) as dag:
    task1 = PythonOperator(
        task_id = "scraping_task",
        python_callable=scrape_nba_task,
        op_args=["{{ ds }}"],
    )
    # # Task 2: Insert NBA games into the database
    # task2 = PythonOperator(
    #     task_id="insert_task",
    #     python_callable=insert_nba_games,
    #     provide_context=True,  # Required to access XCom
    # )

    task1 #>> task2