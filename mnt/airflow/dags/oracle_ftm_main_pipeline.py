import csv

from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

def form_func_call(pair, network):
    with open('/opt/airflow/dags/metadata/ftm-main.csv', 'r') as file:
        reader = csv.reader(file, delimiter=";")
        arr = [row for row in reader]
    function_call = "brownie run scripts/get_asset.py main mysql root root".split(" ")
    function_call.extend(list(filter(lambda x: x[0] == pair, arr))[0])
    function_call.extend(["--network", network])
    var_parms = dict(
        entrypoint=function_call,
        task_id=f"{pair}_chain_data",
        container_name=f"{pair}_chain_data",
    )
    return var_parms



default_args ={
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "marco_aurelio_reis@yahoo.com.br",
    "retries": 1,
    "retry_delay": timedelta(minutes=5) 
}

BASEPATH = "/opt/airflow/dags/"

COMMON_PARMS = dict(
        image="marcoaureliomenezes/chainwatcher:1.2",
        environment={'WEB3_INFURA_PROJECT_ID':'1f6c5d7a4b6b4b5fa11d285a5ed2f552'},
        api_version='auto', 
        docker_url="unix:///var/run/docker.sock",
        network_mode='airflow-network',
        auto_remove=True,
        mount_tmp_dir=False)

with DAG(
            "oracles_fantom_pipeline", 
            start_date=datetime(2022,5,16), 
            schedule_interval='@daily', 
            default_args=default_args, 
            catchup=False
        ) as dag:

    ################################    DEFINE TASK    ##########################################
    start_batch_20min = BashOperator(task_id="start_batch_20min", bash_command="""sleep 2""")
    
    btc_usd_chain_data= DockerOperator(**form_func_call("btc_usd", 'ftm-main'),**COMMON_PARMS)
    eth_usd_chain_data= DockerOperator(**form_func_call("eth_usd", 'ftm-main'),**COMMON_PARMS)
    bnb_usd_chain_data= DockerOperator(**form_func_call("bnb_usd", 'ftm-main'),**COMMON_PARMS)
    ftm_usd_chain_data= DockerOperator(**form_func_call("ftm_usd", 'ftm-main'),**COMMON_PARMS)
    link_usd_chain_data = DockerOperator(**form_func_call("link_usd", 'ftm-main'),**COMMON_PARMS)
    busd_usd_chain_data= DockerOperator(**form_func_call("busd_usd", 'ftm-main'),**COMMON_PARMS)
    dai_usd_chain_data = DockerOperator(**form_func_call("dai_usd", 'ftm-main'), **COMMON_PARMS)
    usdc_usd_chain_data= DockerOperator(**form_func_call("usdc_usd", 'ftm-main'),**COMMON_PARMS)
    usdt_usd_chain_data = DockerOperator(**form_func_call("usdt_usd", 'ftm-main'),**COMMON_PARMS)
    aave_usd_chain_data = DockerOperator(**form_func_call("aave_usd", 'ftm-main'),**COMMON_PARMS)
    boo_usd_chain_data = DockerOperator(**form_func_call("boo_usd", 'ftm-main'),**COMMON_PARMS)
    crv_usd_chain_data = DockerOperator(**form_func_call("crv_usd", 'ftm-main'),**COMMON_PARMS)
    end_batch_20min = BashOperator(task_id="end_batch_20min", bash_command="""sleep 2""")

    ################################    JOB ORDER    ##########################################
    start_batch_20min >> btc_usd_chain_data >>  link_usd_chain_data >> ftm_usd_chain_data >> boo_usd_chain_data >> end_batch_20min
    
    start_batch_20min >> eth_usd_chain_data >> aave_usd_chain_data >> usdt_usd_chain_data >> crv_usd_chain_data >> end_batch_20min

    start_batch_20min >> bnb_usd_chain_data >> dai_usd_chain_data >> busd_usd_chain_data >> usdc_usd_chain_data  >> end_batch_20min