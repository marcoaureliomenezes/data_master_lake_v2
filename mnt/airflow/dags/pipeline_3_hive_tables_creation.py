from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.providers.apache.hive.operators.hive import HiveOperator
from scripts.hive.handle_hive_tables import *


default_args ={
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "marco_aurelio_reis@yahoo.com.br",
    "retries": 1,
    "retry_delay": timedelta(minutes=5) 
}

with DAG("hive_tables_creation_pipeline", start_date=datetime(2021,1,1), schedule_interval="@once", default_args=default_args, catchup=False) as dag:


    start_create_tables = BashOperator(task_id="start_create_tables", bash_command="""sleep 2""")
    end_create_tables = BashOperator(task_id="end_create_tables", bash_command="""sleep 2""")

    create_client_accounts_table = HiveOperator(
        task_id="create_client_accounts_table",
        hive_cli_conn_id="hive_conn",
        hql=create_clients_table
    )



    create_conta_corrente_table = HiveOperator(
        task_id="create_conta_corrente_table",
        hive_cli_conn_id="hive_conn",
        hql=create_product_conta_corrente_table
    )

    create_poupanca_table = HiveOperator(
        task_id="create_poupanca_table",
        hive_cli_conn_id="hive_conn",
        hql=create_product_poupanca_table
    )

    create_seguros_table = HiveOperator(
        task_id="create_seguros_table",
        hive_cli_conn_id="hive_conn",
        hql=create_product_seguros_table
    )

    create_consorcio_table = HiveOperator(
        task_id="create_consorcio_table",
        hive_cli_conn_id="hive_conn",
        hql=create_product_consorcio_table
    )


    create_renda_fixa_table = HiveOperator(
        task_id="create_renda_fixa_table",
        hive_cli_conn_id="hive_conn",
        hql=create_product_renda_fixa_table
    )

    create_renda_variavel_table = HiveOperator(
        task_id="create_renda_variavel_table",
        hive_cli_conn_id="hive_conn",
        hql=create_product_renda_variavel_table
    )

    create_titulos_table = HiveOperator(
        task_id="create_titulos_table",
        hive_cli_conn_id="hive_conn",
        hql=create_product_titulos_table
    )

    create_derivativos_table = HiveOperator(
        task_id="create_derivativos_table",
        hive_cli_conn_id="hive_conn",
        hql=create_product_derivativos_table
    )

    create_assets_stockmarkets_table = HiveOperator(
        task_id="create_assets_stockmarkets_table",
        hive_cli_conn_id="hive_conn",
        hql=create_daily_stock_markets_table
    )

    create_metadata_oracles_table = HiveOperator(
        task_id="create_metadata_oracles_table",
        hive_cli_conn_id="hive_conn",
        hql=create_metadata_oracle_prices
    )

    create_pricefeed_oracles_table = HiveOperator(
        task_id="create_pricefeed_oracles_table",
        hive_cli_conn_id="hive_conn",
        hql=create_oracle_pricefeeds
    )


    start_create_tables >> create_metadata_oracles_table >> create_client_accounts_table >> create_assets_stockmarkets_table >> create_conta_corrente_table >> end_create_tables
    
    start_create_tables  >> create_pricefeed_oracles_table >> create_poupanca_table >> create_seguros_table >> create_consorcio_table >> end_create_tables
    
    start_create_tables >> create_renda_fixa_table >> create_renda_variavel_table >> create_titulos_table >> create_derivativos_table >> end_create_tables