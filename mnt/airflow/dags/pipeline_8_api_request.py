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

with DAG(
            "api_request_pipeline", 
            start_date=datetime(2022,5,16), 
            schedule_interval='* * * * *',
            default_args=default_args, 
            catchup=False
) as dag:


    starting_process = BashOperator(
        task_id="starting_task",
        bash_command="""sleep 2"""
    )


    get_assets_data_from_api= DockerOperator(
        task_id="get_assets_data_from_api",
        container_name="get_assets_data_from_api",
        image="marcoaureliomenezes/batcher:1.0",
        command="python python/get_10min_markets.py --host kafka --port 9092 --topic assets_from_api",
        docker_url="unix:///var/run/docker.sock",
        auto_remove=True,
        mount_tmp_dir=False,
        network_mode='airflow-network'
    )

    end_process = BashOperator(
        task_id="end_process",
        bash_command="""sleep 2"""
    )


    starting_process >> get_assets_data_from_api >> end_process