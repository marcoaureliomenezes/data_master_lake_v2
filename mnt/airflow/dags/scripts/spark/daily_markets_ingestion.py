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


def ingest_product(product_name):
    df = spark.read.parquet(f'hdfs://namenode:9000/daily_markets/{product_name}')

    df = df.withColumnRenamed("date", "data")
    df.printSchema()
    df.write.mode("append").insertInto(f"products.{product_name}", overwrite=False)


asset_groups = ["big_techs", "commodities", "crypto", "ibovespa", "markets", "stablecoins"]

for asset in asset_groups:
    ingest_product(asset)
