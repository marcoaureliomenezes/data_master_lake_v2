from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.http.sensors.http import HttpSensor
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.apache.hive.operators.hive import HiveOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from scripts.hive.handle_hive_tables import *



default_args ={
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "marco_aurelio_reis@yahoo.com.br",
    "retries": 1,
    "retry_delay": timedelta(minutes=5) 
}

with DAG("delete_hive_databases", start_date=datetime(2021,1,1), schedule_interval="@once", default_args=default_args, catchup=False) as dag:


    start_create_tables = BashOperator(task_id="start_create_tables", bash_command="""sleep 2""")
    end_create_tables = BashOperator(task_id="end_create_tables", bash_command="""sleep 2""")

    delete_client_database = HiveOperator(
        task_id="delete_client_database",
        hive_cli_conn_id="hive_conn",
        hql=deleting_clients_database
    )

    delete_products_database = HiveOperator(
        task_id="delete_products_database",
        hive_cli_conn_id="hive_conn",
        hql=deleting_products_database
    )

    delete_daily_markets_database = HiveOperator(
        task_id="delete_daily_markets_database",
        hive_cli_conn_id="hive_conn",
        hql=deleting_daily_markets_database
    )

    delete_oracles_database = HiveOperator(
        task_id="delete_oracles_database",
        hive_cli_conn_id="hive_conn",
        hql=deleting_oracles_database
    )


    start_create_tables  >> delete_client_database >> delete_oracles_database >> delete_products_database >> delete_daily_markets_database >> end_create_tables
    