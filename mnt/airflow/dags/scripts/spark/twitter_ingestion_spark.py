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


schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("userId", IntegerType(), True),
    StructField("geolocation", StringType(), True),
    StructField("retweet_count", IntegerType(), True),
    StructField("texto", StringType(), True),
    StructField("in_reply_to_user_id", IntegerType(), True)
    
    ])
# Read the file forex_rates.json from the HDFS
columns = ['id', 'in_reply_to_user_id', 'place.country', 'place.place_type', 'retweet_count', 'reply_count', 'text', 'timestamp_ms', 'lang']
df = spark.read.json('hdfs://namenode:9000/twitter/santander')
df.printSchema()
df = df.select(*columns)
df = df.filter(col('lang').isin('en', 'pt', 'es', 'de'))

df.show(50, False)
print(df.count())
# result = df.select("id", "userId", "geolocation", "retweet_count", "texto", "in_reply_to_user_id")
# result.show()
# result.write.mode("overwrite").insertInto("marketing.twitter", overwrite=True)