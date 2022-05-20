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
            "oracle_batches_pipeline", 
            start_date=datetime(2022,5,16), 
            schedule_interval='*/5 * * * *', 
            default_args=default_args, 
            catchup=False
        ) as dag:


    start_batch_20min = BashOperator(
        task_id="start_batch_20min",
        bash_command="""sleep 2"""
    )

    eth_chain_data= DockerOperator(
        task_id="eth_chain_data",
        image="marcoaureliomenezes/chainwatcher:1.0",
        command="brownie run scripts/watch_price.py main kafka 9092 eth_chain --network mainnet",
        docker_url="unix:///var/run/docker.sock",
        network_mode='airflow-network'
    )


    bsc_chain_data= DockerOperator(
        task_id="bsc_chain_data",
        image="marcoaureliomenezes/chainwatcher:1.0",
        command="brownie run scripts/watch_price.py main kafka 9092 bsc_chain --network bsc-main",
        docker_url="unix:///var/run/docker.sock",
        mount_tmp_dir=False,
        network_mode='airflow-network'
    )

    ftm_chain_data= DockerOperator(
        task_id="ftm_chain_data",
        image="marcoaureliomenezes/chainwatcher:1.0",
        command="brownie run scripts/watch_price.py main kafka 9092 ftm_chain --network ftm-main",
        docker_url="unix:///var/run/docker.sock",
        network_mode='airflow-network'
    )

    end_batch_20min = BashOperator(
        task_id="end_batch_20min",
        bash_command="""sleep 2"""
    )

    start_batch_20min >> [eth_chain_data, bsc_chain_data, ftm_chain_data] >> end_batch_20min
    