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

with DAG("batch_processes_pipeline", start_date=datetime(2021,1,1), schedule_interval="@daily", default_args=default_args, catchup=False) as dag:


    starting_process = BashOperator(
        task_id="starting_task",
        bash_command="""sleep 2"""
    )
    # command="python gen_clients.py --user root --password root --host mysql --port 3306 --db data_master --size 10000",

    batch_random_data= DockerOperator(
        task_id="batch_random_data",
        image="marcoaureliomenezes/batcher:1.0",
        command="python python/gen_fake_data.py --user root --password root --host mysql --port 3306 --db data_master --size 10000",
        docker_url="unix:///var/run/docker.sock",
        network_mode='airflow-network'
    )


    batch_market_operator= DockerOperator(
        task_id="batch_market_operator",
        image="marcoaureliomenezes/batcher:1.0",
        command="python python/get_daily_markets.py --user root --password root --host mysql --port 3306 --db data_master --period max",
        docker_url="unix:///var/run/docker.sock",
        network_mode='airflow-network'
    )


    starting_process >> batch_random_data >> batch_market_operator
    