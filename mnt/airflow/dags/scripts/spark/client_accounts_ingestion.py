from os.path import abspath

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

warehouse_location = abspath('spark-warehouse')

# Initialize Spark Session
spark = SparkSession \
    .builder \
    .appName("Forex processing") \
    .config("spark.sql.warehouse.dir", warehouse_location) \
    .config("spark.driver.memory", "10G") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sparkContext.setLogLevel('ERROR')



# Read the file forex_rates.json from the HDFS
df_client_accounts = spark.read.parquet('hdfs://namenode:9000/clients/accounts/')
df_client_accounts.printSchema()
df_client_accounts.write.mode("overwrite").insertInto("clients.accounts", overwrite=True)


def ingest_product(product_name):
    df = spark.read.parquet(f'hdfs://namenode:9000/clients/products/{product_name}')
    df.printSchema()
    df.write.mode("overwrite").insertInto(f"products.{product_name}", overwrite=True)

