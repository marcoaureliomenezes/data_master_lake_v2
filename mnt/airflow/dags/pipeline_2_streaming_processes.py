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

COMMON_PARMS = dict(
        image="marcoaureliomenezes/streamers:1.2",
        environment={
            'KAFKA_SERVICE': 'kafka',
            'KAFKA_PORT': '9092',
            'MYSQL_SERVICE': 'mysql',
            'MYSQL_USER': 'root',
            'MYSQL_PASS': 'root',
        },
        api_version='auto', 
        docker_url="unix:///var/run/docker.sock",
        network_mode='airflow-network',
        auto_remove=True,
        mount_tmp_dir=False)

def gen_variable_parms(method, freq, topic):
    return dict(
        task_id=f"streaming_{topic}_operations",
        container_name=f"streaming_{topic}_operations",
        entrypoint=f"python main.py method={method} freq={freq} database=rand_engine_data table=cli_accounts topic={topic}".split(" "),
    )

with DAG("streaming_processes_pipeline", start_date=datetime(2021,1,1), schedule_interval="@daily", default_args=default_args, catchup=False) as dag:

    starting_process = BashOperator(
        task_id="starting_process",
        bash_command="""sleep 2"""
    )

    streaming_bills_operations= DockerOperator(
        **gen_variable_parms(method='gen_bill_operation', freq=1000, topic='bills_generation'),
        **COMMON_PARMS
    )


    streaming_credCard_operations= DockerOperator(
        **gen_variable_parms(method='gen_creditCard_operation', freq=10, topic='credit_card_operations'),
        **COMMON_PARMS
    )

    streaming_pix_operations= DockerOperator(
        **gen_variable_parms(method='gen_pix_operation', freq=10, topic='pix_operations'),
        **COMMON_PARMS
    )



    starting_process >> [streaming_bills_operations, streaming_credCard_operations, streaming_pix_operations]
    