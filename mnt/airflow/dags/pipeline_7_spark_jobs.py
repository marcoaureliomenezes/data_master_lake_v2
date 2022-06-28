from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator


default_args ={
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "marco_aurelio_reis@yahoo.com.br",
    "retries": 1,
    "retry_delay": timedelta(minutes=5) 
}

with DAG("spark_jobs_pipeline", start_date=datetime(2021,1,1), schedule_interval="@daily", default_args=default_args, catchup=False) as dag:


 
    # twitter_ingestion_job = SparkSubmitOperator(
    #     task_id="twitter_ingestion_job",
    #     application="/opt/airflow/dags/scripts/spark/twitter_ingestion_spark.py",
    #     conn_id="spark_conn",
    #     verbose=False
    # )
    
    start_batch_20min = BashOperator(task_id="start_batch_20min", bash_command="""sleep 2""")
    end_batch_20min = BashOperator(task_id="end_batch_20min", bash_command="""sleep 2""")

    ingesting_client_accounts = SparkSubmitOperator(
        task_id="ingesting_client_accounts",
        application="/opt/airflow/dags/scripts/spark/client_accounts_ingestion.py",
        conn_id="spark_conn",
        verbose=False
    )

    ingesting_client_products = SparkSubmitOperator(
        task_id="ingesting_client_products",
        application="/opt/airflow/dags/scripts/spark/client_products_ingestion.py",
        conn_id="spark_conn",
        verbose=False
    )

    ingesting_daily_markets = SparkSubmitOperator(
        task_id="ingesting_daily_markets",
        application="/opt/airflow/dags/scripts/spark/daily_markets_ingestion.py",
        conn_id="spark_conn",
        verbose=False
    )


    start_batch_20min >> ingesting_client_accounts >> ingesting_client_products >> ingesting_daily_markets >> end_batch_20min 