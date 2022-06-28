from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
import csv
from functools import reduce



default_args ={
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "marco_aurelio_reis@yahoo.com.br",
    "retries": 1,
    "retry_delay": timedelta(minutes=5) 
}

PATH_YAHOO_TICKERS = '/opt/airflow/dags/metadata/yahoo_tickers.csv'

def gen_assets_jobs_attributes(asset_group, file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=";")
        arr = [row for row in reader]
    filtered_asset_group = list(filter(lambda x: x[2] == asset_group, arr))
    filtered_assets = [asset[0] for asset in filtered_asset_group]
    fixed = "python get_daily_markets.py period=max database=daily_markets"
    variable = f"table={asset_group} asset_group={reduce(lambda a, b: f'{a},{b}', filtered_assets)}"
    result = dict(
        entrypoint = f"{fixed} {variable}".split(" "),
        task_id = f'asset_group_{asset_group}',
        container_name = f'asset_group_{asset_group}',
    )
    return result


COMMON_PARMS = dict(
        image="marcoaureliomenezes/batcher:1.1",
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



with DAG("initial_batch_pipeline", start_date=datetime(2021,1,1), schedule_interval="@once", default_args=default_args, catchup=False) as dag:


    starting_process = BashOperator(
        task_id="starting_task",
        bash_command="""sleep 2"""
    )

    create_client_accounts= DockerOperator(
        task_id="create_client_accounts",
        container_name="create_client_accounts",
        entrypoint="python gen_client_accounts.py size=100000 database=rand_engine_data table=cli_accounts".split(" "),
        **COMMON_PARMS
    )

    create_cli_prod_distribution= DockerOperator(
        task_id="create_cli_prod_distribution",
        container_name="create_cli_prod_distribution",
        entrypoint="python gen_cli_prod_distribution.py database=rand_engine_data input_table=cli_accounts output_table=cli_prod_distro".split(" "),
        **COMMON_PARMS
    )

    create_cli_prod_derivativos= DockerOperator(
        task_id="create_cli_prod_derivativos",
        container_name="create_cli_prod_derivativos",
        entrypoint="python gen_client_products.py database=rand_engine_data input_table=cli_prod_distro output_table=derivativos".split(" "),
        **COMMON_PARMS
    )


    create_cli_prod_conta_corrente= DockerOperator(
        task_id="create_cli_prod_conta_corrente",
        container_name="create_cli_prod_conta_corrente",
        entrypoint="python gen_client_products.py database=rand_engine_data input_table=cli_prod_distro output_table=conta_corrente".split(" "),
        **COMMON_PARMS
    )    
    
    create_cli_prod_poupanca= DockerOperator(
        task_id="create_cli_prod_poupanca",
        container_name="create_cli_prod_poupanca",
        entrypoint="python gen_client_products.py database=rand_engine_data input_table=cli_prod_distro output_table=poupanca".split(" "),
        **COMMON_PARMS
    )   
    
    create_cli_prod_consorcio= DockerOperator(
        task_id="create_cli_prod_consorcio",
        container_name="create_cli_prod_consorcio",
        entrypoint="python gen_client_products.py database=rand_engine_data input_table=cli_prod_distro output_table=consorcio".split(" "),
        **COMMON_PARMS
    )

    create_cli_prod_seguros= DockerOperator(
        task_id="create_cli_prod_seguros",
        container_name="create_cli_prod_seguros",
        entrypoint="python gen_client_products.py database=rand_engine_data input_table=cli_prod_distro output_table=seguros".split(" "),
        **COMMON_PARMS
    )

    create_cli_prod_titulos= DockerOperator(
        task_id="create_cli_prod_titulos",
        container_name="create_cli_prod_titulos",
        entrypoint="python gen_client_products.py database=rand_engine_data input_table=cli_prod_distro output_table=titulos".split(" "),
        **COMMON_PARMS
    )   
    
    
    create_cli_prod_renda_fixa= DockerOperator(
        task_id="create_cli_prod_renda_fixa",
        container_name="create_cli_prod_renda_fixa",
        entrypoint="python gen_client_products.py database=rand_engine_data input_table=cli_prod_distro output_table=renda_fixa".split(" "),
        **COMMON_PARMS
    )

    create_cli_prod_renda_variavel= DockerOperator(
        task_id="create_cli_prod_renda_variavel",
        container_name="create_cli_prod_renda_variavel",
        entrypoint="python gen_client_products.py database=rand_engine_data input_table=cli_prod_distro output_table=renda_variavel".split(" "),
        **COMMON_PARMS
    )
  
    asset_group_markets= DockerOperator(
        **gen_assets_jobs_attributes('markets', PATH_YAHOO_TICKERS),  
        **COMMON_PARMS
    )

    asset_group_ibovespa= DockerOperator(
        **gen_assets_jobs_attributes('ibovespa', PATH_YAHOO_TICKERS),  
        **COMMON_PARMS
    )

    asset_group_big_techs= DockerOperator(
        **gen_assets_jobs_attributes('big_techs', PATH_YAHOO_TICKERS),  
        **COMMON_PARMS
    )

    asset_group_commodities= DockerOperator(
        **gen_assets_jobs_attributes('commodities', PATH_YAHOO_TICKERS), 
        **COMMON_PARMS
    )

    asset_group_crypto= DockerOperator(
        **gen_assets_jobs_attributes('crypto', PATH_YAHOO_TICKERS),  
        **COMMON_PARMS
    )

    asset_group_stablecoins= DockerOperator(
        **gen_assets_jobs_attributes('stablecoins', PATH_YAHOO_TICKERS),  
        **COMMON_PARMS
    )

    end_process = BashOperator(
        task_id="end_task",
        bash_command="""sleep 2"""
    )

    starting_process >> create_client_accounts >> create_cli_prod_distribution

    create_cli_prod_distribution >> create_cli_prod_conta_corrente >> create_cli_prod_poupanca >> end_process

    create_cli_prod_distribution >> create_cli_prod_renda_fixa >> create_cli_prod_renda_variavel >> end_process
    
    create_cli_prod_distribution >> create_cli_prod_seguros >> create_cli_prod_consorcio >> end_process

    create_cli_prod_distribution >> create_cli_prod_titulos >> create_cli_prod_derivativos >> end_process


    starting_process >> asset_group_markets >> asset_group_ibovespa >> asset_group_big_techs >> asset_group_commodities >> asset_group_crypto >> asset_group_stablecoins >> end_process


