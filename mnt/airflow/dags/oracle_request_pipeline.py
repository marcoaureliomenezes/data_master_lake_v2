from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args ={
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "marco_aurelio_reis@yahoo.com.br",
    "retries": 1,
    "retry_delay": timedelta(minutes=5) 
}

BASEPATH = "/opt/airflow/dags/"

with DAG(
            "oracle_batches_pipeline", 
            start_date=datetime(2022,5,16), 
            schedule_interval='@daily', 
            default_args=default_args, 
            catchup=False
        ) as dag:


    start_batch_20min = BashOperator(
        task_id="start_batch_20min",
        bash_command="""sleep 2"""
    )


    eth_chain_data= DockerOperator(
        image="marcoaureliomenezes/chainwatcher:1.0",
        task_id="eth_chain_data",
        container_name="eth_chain_data",
        api_version='auto',
        environment={'WEB3_INFURA_PROJECT_ID':'1f6c5d7a4b6b4b5fa11d285a5ed2f552',
        "WEB3_ALCHEMY_PROJECT_ID": "DZGXon_D4DBNqFnvaP_6yGOAyyknkNtH"},
        entrypoint=["brownie", "run", "scripts/get_historical.py", "main", "mysql", "root", "root", "--network", "mainnet"],
        docker_url="unix:///var/run/docker.sock",
        network_mode='airflow-network',
        auto_remove=True,
        mount_tmp_dir=False,
    )

    bsc_chain_data= DockerOperator(
        image="marcoaureliomenezes/chainwatcher:1.0",
        task_id="bsc_chain_data",
        container_name="bsc_chain_data",
        api_version='auto',
        environment={'WEB3_INFURA_PROJECT_ID':'1f6c5d7a4b6b4b5fa11d285a5ed2f552',
        "WEB3_ALCHEMY_PROJECT_ID": "DZGXon_D4DBNqFnvaP_6yGOAyyknkNtH"},
        #entrypoint=["brownie", "run", "scripts/get_historical.py", "main", "mysql", "root", "root", "--network", "bsc-main"],
        command = "brownie run scripts/get_historical.py main mysql root root --network bsc-main",
        docker_url="unix:///var/run/docker.sock",
        network_mode='airflow-network',
        auto_remove=True,
        mount_tmp_dir=False

    )

    ftm_chain_data= DockerOperator(
        image="marcoaureliomenezes/chainwatcher:1.0",
        task_id="ftm_chain_data",
        container_name="ftm_chain_data",
        api_version='auto',
        environment={'WEB3_INFURA_PROJECT_ID':'1f6c5d7a4b6b4b5fa11d285a5ed2f552',
        "WEB3_ALCHEMY_PROJECT_ID": "DZGXon_D4DBNqFnvaP_6yGOAyyknkNtH"},
        entrypoint=["brownie", "run", "scripts/get_historical.py", "main", "mysql", "root", "root", "--network", "ftm-main"],
        docker_url="unix:///var/run/docker.sock",
        network_mode='airflow-network',
        auto_remove=True,
        mount_tmp_dir=False
    )

    end_batch_20min = BashOperator(
        task_id="end_batch_20min",
        bash_command="""sleep 2"""
    )

    start_batch_20min >> [ftm_chain_data , eth_chain_data , bsc_chain_data] >> end_batch_20min
    