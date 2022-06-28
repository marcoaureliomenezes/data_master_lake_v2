from os.path import abspath

from pyspark.sql import SparkSession
from pyspark.sql.functions import lit

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
spark.conf.set("hive.exec.dynamic.partition.mode", "nonstrict")

def ingest_product(asset_group):
    df = spark.read.parquet(f'hdfs://namenode:9000/daily_markets/{asset_group}')

    df = df.withColumnRenamed("date", "data")
    df = df.withColumn("asset_group", lit(asset_group))
    df.printSchema()
    df.write.mode("append").insertInto(f"daily_stock_markets.assets", overwrite=False)


asset_groups = ["big_techs", "commodities", "crypto", "ibovespa", "markets", "stablecoins"]

for asset in asset_groups:
    ingest_product(asset)
