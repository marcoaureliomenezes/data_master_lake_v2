from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator

default_args ={
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "marco_aurelio_reis@yahoo.com.br",
    "retries": 1,
    "retry_delay": timedelta(minutes=5) 
}

with DAG("streaming_processes_pipeline", start_date=datetime(2021,1,1), schedule_interval="@daily", default_args=default_args, catchup=False) as dag:


    starting_process = BashOperator(
        task_id="starting_process",
        bash_command="""sleep 2"""
    )

    streaming_bills_operations= DockerOperator(
        task_id="streaming_bills_operations",
        image="marcoaureliomenezes/streamers:1.0",
        command="python streaming_bills.py --host kafka --port 9092 --freq 1 --num_clients 1000000",
        docker_url="unix:///var/run/docker.sock",
        network_mode='airflow-network'
    )

    streaming_CDBs_operations= DockerOperator(
        task_id="streaming_CDBs_operations",
        image="marcoaureliomenezes/streamers:1.0",
        command="python streaming_CDBs.py --host kafka --port 9092 --freq 1 --num_clients 1000000",
        docker_url="unix:///var/run/docker.sock",
        network_mode='airflow-network'
    )

    streaming_credCard_operations= DockerOperator(
        task_id="streaming_credCard_operations",
        image="marcoaureliomenezes/streamers:1.0",
        command="python streaming_creditcard.py --host kafka --port 9092 --freq 1 --num_clients 1000000",
        docker_url="unix:///var/run/docker.sock",
        network_mode='airflow-network'
    )

    streaming_pix_operations= DockerOperator(
        task_id="streaming_pix_operations",
        image="marcoaureliomenezes/streamers:1.0",
        command="python streaming_pix.py --host kafka --port 9092 --freq 1 --num_clients 1000000",
        docker_url="unix:///var/run/docker.sock",
        network_mode='airflow-network'
    )

    streaming_stocks_operations= DockerOperator(
        task_id="streaming_stocks_operations",
        image="marcoaureliomenezes/streamers:1.0",
        command="python streaming_stocks.py --host kafka --port 9092 --freq 1 --num_clients 1000000",
        docker_url="unix:///var/run/docker.sock",
        network_mode='airflow-network'
    )

    streaming_problem = BashOperator(
        task_id="streaming_problem",
        bash_command="""sleep 2"""
    )

    starting_process >> [streaming_bills_operations, streaming_CDBs_operations, streaming_credCard_operations, streaming_pix_operations, streaming_stocks_operations] >> streaming_problem
    