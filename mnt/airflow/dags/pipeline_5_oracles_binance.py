import csv
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from functools import reduce


def form_func_call(pair, network, factor='1'):
    BASEPATH = "/opt/airflow/dags"
    file_metadata = f'{BASEPATH}/metadata/{network}.csv'
    with open(file_metadata, 'r') as file:
        reader = csv.reader(file, delimiter=";")
        arr = [row for row in reader]
    pair_address = reduce(lambda a,b: f'{a} {b}', list(filter(lambda x: x[0] == pair, arr))[0])
    network_active = f"--network {network}"
    function_call = f"brownie run scripts/get_asset.py main {pair_address} {factor} {network_active}"
    return dict(
        entrypoint=function_call.split(),
        task_id=f"{pair}_{network}",
        container_name=f"{pair}_{network}_container",
    )

default_args ={
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "marco_aurelio_reis@yahoo.com.br",
    "retries": 1,
    "retry_delay": timedelta(minutes=5) 
}

COMMON_PARMS = dict(
        image="marcoaureliomenezes/chainwatcher:1.3",
        environment={
            'MYSQL_SERVICE': 'mysql',
            'MYSQL_USER': 'root',
            'MYSQL_PASS': 'root',
        },
        api_version='auto', 
        docker_url="unix:///var/run/docker.sock",
        network_mode='airflow-network',
        auto_remove=True,
        mount_tmp_dir=False)

with DAG(
            "oracles_binance_pipeline", 
            start_date=datetime(2022,5,16), 
            schedule_interval='@daily', 
            default_args=default_args, 
            catchup=False
        ) as dag:

    ################################    DEFINE TASK    ##########################################
    start_batch_20min = BashOperator(task_id="start_batch_20min", bash_command="""sleep 2""")

    btc_usd_job= DockerOperator(**form_func_call("btc_usd", 'bsc-main'),**COMMON_PARMS)
    eth_usd_job= DockerOperator(**form_func_call("eth_usd", 'bsc-main'),**COMMON_PARMS)
    sol_usd_job= DockerOperator(**form_func_call("sol_usd", 'bsc-main'),**COMMON_PARMS)
    bnb_usd_job= DockerOperator(**form_func_call("bnb_usd", 'bsc-main'),**COMMON_PARMS)
    ada_usd_job= DockerOperator(**form_func_call("ada_usd", 'bsc-main'),**COMMON_PARMS)
    avax_usd_job= DockerOperator(**form_func_call("avax_usd", 'bsc-main'),**COMMON_PARMS)
    dot_usd_job= DockerOperator(**form_func_call("dot_usd", 'bsc-main'),**COMMON_PARMS)
    ftm_usd_job= DockerOperator(**form_func_call("ftm_usd", 'bsc-main'),**COMMON_PARMS)
    matic_usd_job = DockerOperator(**form_func_call("matic_usd", 'bsc-main'),**COMMON_PARMS)
    doge_usd_job = DockerOperator(**form_func_call("doge_usd", 'bsc-main'),**COMMON_PARMS)
    dai_usd_job = DockerOperator(**form_func_call("dai_usd", 'bsc-main'), **COMMON_PARMS)
    busd_usd_job= DockerOperator(**form_func_call("busd_usd", 'bsc-main'),**COMMON_PARMS)
    usdc_usd_job= DockerOperator(**form_func_call("usdc_usd", 'bsc-main'),**COMMON_PARMS)
    usdt_usd_job = DockerOperator(**form_func_call("usdt_usd", 'bsc-main'),**COMMON_PARMS)
    

    end_batch_20min = BashOperator(task_id="end_batch_20min", bash_command="""sleep 2""")

    ################################    JOB ORDER    ##########################################
    start_batch_20min >> btc_usd_job >> sol_usd_job >> busd_usd_job >> end_batch_20min

    start_batch_20min >> eth_usd_job >> doge_usd_job >> avax_usd_job >> end_batch_20min
    start_batch_20min >> bnb_usd_job >> ada_usd_job >> end_batch_20min
    
    start_batch_20min >> dot_usd_job >> ftm_usd_job >> dai_usd_job >> end_batch_20min
    start_batch_20min >> matic_usd_job >> usdc_usd_job >> usdt_usd_job >> end_batch_20min



