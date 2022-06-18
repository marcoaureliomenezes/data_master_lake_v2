import csv

from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

def form_func_call(pair, network):
    with open('/opt/airflow/dags/metadata/mainnet.csv', 'r') as file:
        reader = csv.reader(file, delimiter=";")
        arr = [row for row in reader]
    function_call = "brownie run scripts/get_asset.py main mysql root root".split(" ")
    function_call.extend(list(filter(lambda x: x[0] == pair, arr))[0])
    function_call.extend(["--network", network])
    var_parms = dict(
        entrypoint=function_call,
        task_id=f"{pair}_chain_data_{network}",
        container_name=f"{pair}_chain_data_{network}",
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
            "oracles_ethereum_pipeline", 
            start_date=datetime(2022,5,16), 
            schedule_interval='@daily', 
            default_args=default_args, 
            catchup=False
        ) as dag:

    ################################    DEFINE TASK    ##########################################
    start_batch_20min = BashOperator(task_id="start_batch_20min", bash_command="""sleep 2""")

    btc_usd_job= DockerOperator(**form_func_call("btc_usd", 'mainnet'),**COMMON_PARMS)
    eth_usd_job= DockerOperator(**form_func_call("eth_usd", 'mainnet'),**COMMON_PARMS)
    sol_usd_job= DockerOperator(**form_func_call("sol_usd", 'mainnet'),**COMMON_PARMS)
    bnb_usd_job= DockerOperator(**form_func_call("bnb_usd", 'mainnet'),**COMMON_PARMS)
    ada_usd_job= DockerOperator(**form_func_call("ada_usd", 'mainnet'),**COMMON_PARMS)
    avax_usd_job= DockerOperator(**form_func_call("avax_usd", 'mainnet'),**COMMON_PARMS)
    link_usd_job= DockerOperator(**form_func_call("link_usd", 'mainnet'),**COMMON_PARMS)
    dot_usd_job= DockerOperator(**form_func_call("dot_usd", 'mainnet'),**COMMON_PARMS)
    ftm_eth_job= DockerOperator(**form_func_call("ftm_eth", 'mainnet'),**COMMON_PARMS)
    matic_usd_job = DockerOperator(**form_func_call("matic_usd", 'mainnet'),**COMMON_PARMS)
    doge_usd_job = DockerOperator(**form_func_call("doge_usd", 'mainnet'),**COMMON_PARMS)

    aave_eth_job = DockerOperator(**form_func_call("aave_eth", 'mainnet'),**COMMON_PARMS)
    aave_usd_job = DockerOperator(**form_func_call("aave_usd", 'mainnet'),**COMMON_PARMS)
    dydx_usd_job = DockerOperator(**form_func_call("dydx_usd", 'mainnet'),**COMMON_PARMS)
    dai_usd_job = DockerOperator(**form_func_call("dai_usd", 'mainnet'), **COMMON_PARMS)
    busd_usd_job= DockerOperator(**form_func_call("busd_usd", 'mainnet'),**COMMON_PARMS)
    usdc_usd_job= DockerOperator(**form_func_call("usdc_usd", 'mainnet'),**COMMON_PARMS)
    usdt_usd_job = DockerOperator(**form_func_call("usdt_usd", 'mainnet'),**COMMON_PARMS)
    wbtc_btc_job = DockerOperator(**form_func_call("wbtc_btc", 'mainnet'),**COMMON_PARMS)

    amzn_usd_job = DockerOperator(**form_func_call("amzn_usd", 'mainnet'),**COMMON_PARMS)
    aapl_usd_job = DockerOperator(**form_func_call("aapl_usd", 'mainnet'),**COMMON_PARMS)
    googl_usd_job = DockerOperator(**form_func_call("googl_usd", 'mainnet'),**COMMON_PARMS)
    tsla_usd_job = DockerOperator(**form_func_call("tsla_usd", 'mainnet'), **COMMON_PARMS)
    oil_usd_job = DockerOperator(**form_func_call("oil_usd", 'mainnet'),**COMMON_PARMS)
    silver_usd_job = DockerOperator(**form_func_call("silver_usd", 'mainnet'),**COMMON_PARMS)
    gold_usd_job = DockerOperator(**form_func_call("gold_usd", 'mainnet'), **COMMON_PARMS)

    end_batch_20min = BashOperator(task_id="end_batch_20min", bash_command="""sleep 2""")

    ################################    JOB ORDER    ##########################################
    start_batch_20min >> btc_usd_job >> sol_usd_job >> bnb_usd_job >> ada_usd_job >> avax_usd_job >> end_batch_20min

    
    start_batch_20min >> eth_usd_job >> link_usd_job >> dot_usd_job >> matic_usd_job >> doge_usd_job >> ftm_eth_job >> end_batch_20min


    start_batch_20min >> aave_eth_job >> aave_usd_job >> dydx_usd_job >> end_batch_20min

    start_batch_20min >> dai_usd_job >> busd_usd_job >> usdc_usd_job >> usdt_usd_job >> wbtc_btc_job >> end_batch_20min

    start_batch_20min >> amzn_usd_job >> aapl_usd_job >> googl_usd_job >> tsla_usd_job >> oil_usd_job >> silver_usd_job >> gold_usd_job >> end_batch_20min

