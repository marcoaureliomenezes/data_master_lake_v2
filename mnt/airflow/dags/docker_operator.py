from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.http.sensors.http import HttpSensor
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.apache.hive.operators.hive import HiveOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from scripts.python_data_generators.populate_mongo import populate_nubank_mongodb_operations, \
                            populate_nubank_mongodb_clients, populate_nubank_mongodb_employees, \
                            populate_public_mongodb_facebook_survey, populate_public_mongodb_survey

from scripts.hive.create_nubank_tables import create_clients_table, create_employees_table, \
                                                create_operations_table, drop_nubank_database
from scripts.hive.create_marketing_tables import create_facebook_table, create_public_survey_table, drop_marketing_database, create_twitter_table


default_args ={
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "marco_aurelio_reis@yahoo.com.br",
    "retries": 1,
    "retry_delay": timedelta(minutes=5) 
}

with DAG("mongo_ingestion_pipeline", start_date=datetime(2021,1,1), schedule_interval="@daily", default_args=default_args, catchup=False) as dag:


    starting_nubank_acquisition_ingestion = BashOperator(
        task_id="starting_nubank_acquisition_ingestion",
        bash_command="""sleep 10"""
    )

    populate_nubank_mongo_operations= PythonOperator(
        task_id="populate_nubank_mongo_operations",
        python_callable=populate_nubank_mongodb_operations,
        op_kwargs={"host":"mongo", "port": 27017, "db": "nubank_data", "collection": "operations", "num_rows": 20000}
    )

    populate_nubank_mongo_clients= PythonOperator(
        task_id="populate_nubank_mongo_clients",
        python_callable=populate_nubank_mongodb_clients,
        op_kwargs={"host":"mongo", "port": 27017, "db": "nubank_data", "collection": "clients", "num_rows": 5000}
    )

    populate_nubank_mongo_employees= PythonOperator(
        task_id="populate_nubank_mongo_employees",
        python_callable=populate_nubank_mongodb_employees,
        op_kwargs={"host":"mongo", "port": 27017, "db": "nubank_data", "collection": "employees", "num_rows":5000}

    )

    end_nubank_mongo_data_ingestion = BashOperator(
        task_id="end_nubank_mongo_data_ingestion",
        bash_command="""sleep 3"""
    )

    ##############################    HIVE    #######################################

    dropping_nubank_db = HiveOperator(
        task_id="dropping_nubank_db",
        hive_cli_conn_id="hive_conn",
        hql=drop_nubank_database
    )
    creating_nubank_client_table = HiveOperator(
        task_id="creating_nubank_client_table",
        hive_cli_conn_id="hive_conn",
        hql=create_clients_table
    )

    creating_nubank_employee_table = HiveOperator(
        task_id="creating_nubank_employee_table",
        hive_cli_conn_id="hive_conn",
        hql=create_employees_table
    )

    creating_nubank_operation_table = HiveOperator(
        task_id="creating_nubank_operation_table",
        hive_cli_conn_id="hive_conn",
        hql=create_operations_table
    )


    end_nubank_tables_creation = BashOperator(
        task_id="end_nubank_tables_creation",
        bash_command="""sleep 3"""
    )
    ###################################################################################

    processing_nubank_acquisition_clients= SparkSubmitOperator(
        task_id="processing_nubank_acquisition_clients",
        application="/opt/airflow/dags/scripts/spark/mongo_acquisition_clients_ingestion.py",
        conn_id="spark_conn",
        packages="org.mongodb.spark:mongo-spark-connector_2.11:2.2.0",
        verbose=False
    )

    processing_nubank_acquisition_employees= SparkSubmitOperator(
        task_id="processing_nubank_acquisition_employees",
        application="/opt/airflow/dags/scripts/spark/mongo_acquisition_employees_ingestion.py",
        conn_id="spark_conn",
        packages="org.mongodb.spark:mongo-spark-connector_2.11:2.2.0",
        verbose=False
    )

    processing_nubank_acquisition_operations= SparkSubmitOperator(
        task_id="processing_nubank_acquisition_operations",
        application="/opt/airflow/dags/scripts/spark/mongo_acquisition_operations_ingestion.py",
        conn_id="spark_conn",
        packages="org.mongodb.spark:mongo-spark-connector_2.11:2.2.0",
        verbose=False
    )

    starting_marketing_data_ingestion = BashOperator(
        task_id="starting_marketing_data_ingestion",
        bash_command="""sleep 10"""
    )
    populate_public_mongo_survey= PythonOperator(
        task_id="populate_public_mongo_survey",
        python_callable=populate_public_mongodb_survey,
        op_kwargs={"host":"mongo", "port": 27017, "db": "santander_marketing", "collection": "public_survey", "num_rows": 10000}
    )

    populate_facebook_mongo_survey= PythonOperator(
        task_id="populate_facebook_mongo_survey",
        python_callable=populate_public_mongodb_facebook_survey,
        op_kwargs={"host":"mongo", "port": 27017, "db": "santander_marketing", "collection": "facebook", "num_rows":10000}
    )


    end_marketing_mongo_collections_ingestion= BashOperator(
        task_id="end_marketing_mongo_collections_ingestion",
        bash_command="""sleep 3"""
    )

    #####################    HIVE MARKETING TABLES CREATION   ############################

    dropping_hive_marketing_database = HiveOperator(
        task_id="dropping_hive_marketing_database",
        hive_cli_conn_id="hive_conn",
        hql=drop_marketing_database
    )

    creating_hive_facebook_table = HiveOperator(
        task_id="creating_facebook_table",
        hive_cli_conn_id="hive_conn",
        hql=create_facebook_table
    )
    creating_hive_public_survey_table = HiveOperator(
        task_id="creating_public_survey_table",
        hive_cli_conn_id="hive_conn",
        hql=create_public_survey_table
    )

    end_marketing_tables_creation= BashOperator(
        task_id="end_marketing_tables_creation",
        bash_command="""sleep 3"""
    )

    ####################    INGESTING DATA INTO MARKETING TABLES    #########################
    
    processing_marketing_facebook_data= SparkSubmitOperator(
        task_id="processing_marketing_facebook_data",
        application="/opt/airflow/dags/scripts/spark/mongo_marketing_facebook_ingestion.py",
        conn_id="spark_conn",
        packages="org.mongodb.spark:mongo-spark-connector_2.11:2.2.0",
        verbose=False
    )

    processing_marketing_public_survey_data= SparkSubmitOperator(
        task_id="processing_marketing_public_survey_data",
        application="/opt/airflow/dags/scripts/spark/mongo_marketing_public_survey_ingestion.py",
        conn_id="spark_conn",
        packages="org.mongodb.spark:mongo-spark-connector_2.11:2.2.0",
        verbose=False
    )

    end_marketing_data_ingestion = BashOperator(
        task_id="end_marketing_data_ingestion",
        bash_command="""sleep 5"""
    )

    end_mongo_pipeline = BashOperator(
        task_id="end_mongo_pipeline",
        bash_command="""sleep 2"""
    )

    start_mongo_pipeline = BashOperator(
        task_id="start_mongo_pipeline",
        bash_command="""sleep 2"""
    )
    # MONGO
    start_mongo_pipeline >> starting_nubank_acquisition_ingestion >> [populate_nubank_mongo_operations, populate_nubank_mongo_clients, populate_nubank_mongo_employees] >> end_nubank_mongo_data_ingestion
    end_nubank_mongo_data_ingestion >> dropping_nubank_db >> [creating_nubank_client_table, creating_nubank_employee_table, creating_nubank_operation_table] >> end_nubank_tables_creation
    
    end_nubank_tables_creation >> processing_nubank_acquisition_clients >> processing_nubank_acquisition_employees >> processing_nubank_acquisition_operations >> end_mongo_pipeline
    
    start_mongo_pipeline >> starting_marketing_data_ingestion >> [populate_public_mongo_survey, populate_facebook_mongo_survey] >> end_marketing_mongo_collections_ingestion >> dropping_hive_marketing_database >> [creating_hive_facebook_table, creating_hive_public_survey_table] >> end_marketing_tables_creation >> processing_marketing_facebook_data >> processing_marketing_public_survey_data >> end_marketing_data_ingestion >> end_mongo_pipeline
 
    # download_twitter_santander_data >> putting_twitter_santander_data >> creating_twitter_santander_table >> marketing_ingestion