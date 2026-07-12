from pyspark.sql import SparkSession, functions as F
import argparse

p=argparse.ArgumentParser()
p.add_argument("--input",required=True)
p.add_argument("--output",required=True)
args=p.parse_args()

spark=SparkSession.builder.appName("customer-events-etl").getOrCreate()
df=spark.read.option("header",True).option("inferSchema",True).csv(args.input)
curated=(df.withColumn("event_date",F.to_date("event_ts"))
          .withColumn("revenue",F.when(F.col("event_type")=="purchase",F.col("amount")).otherwise(F.lit(0.0)))
          .groupBy("event_date","region","event_type")
          .agg(F.count("*").alias("event_count"),F.sum("revenue").alias("revenue")))
curated.write.mode("overwrite").partitionBy("event_date").parquet(args.output)
spark.stop()
