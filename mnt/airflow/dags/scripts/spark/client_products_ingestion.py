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
    df = spark.read.parquet(f'hdfs://namenode:9000/clients/products/{product_name}')
    df.printSchema()
    df.write.mode("overwrite").insertInto(f"products.{product_name}", overwrite=True)


products = ["poupanca", "seguros", "consorcio", "renda_variavel", "renda_fixa", "titulos", "derivativos"]

for product in products:
    ingest_product(product)
