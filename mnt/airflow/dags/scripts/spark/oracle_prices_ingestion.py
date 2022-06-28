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

def ingest_asset(network, assets):
    for asset in assets:
        print(asset, network)
        df = spark.read.parquet(f'hdfs://namenode:9000/oracles/{network}/{asset}')
        df = df.withColumn('pair', lit(asset))
        df = df.withColumn('network', lit(network))
        df.printSchema()
    df.write.mode("append").insertInto(f"oracles.pricefeeds", overwrite=False)



binance_tables = ["ada_usd","avax_usd","btc_usd","busd_usd","dai_usd","dot_usd","eth_usd","ftm_usd","matic_usd","sol_usd","usdc_usd","usdt_usd"]

fantom_tables =  ["aave_usd", "bnb_usd", "boo_usd", "btc_usd", "busd_usd", "crv_usd", "dai_usd", "eth_usd", "ftm_usd", "link_usd", "usdc_usd", "usdt_usd"]
ethereum_tables = ["aapl_usd", "ada_usd", "amzn_usd", "avax_usd", "bnb_usd", "btc_usd", "doge_usd", "eth_usd", "gold_usd", "googl_usd", "oil_usd", "silver_usd", "tsla_usd"]
 
dict_chains = {'binance': binance_tables, 'fantom': fantom_tables, 'ethereum': ethereum_tables}

for network, assets in dict_chains.items():
    ingest_asset(network, assets)
