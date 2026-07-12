from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.clustering import KMeans
from pyspark.ml import Pipeline
import argparse

p=argparse.ArgumentParser()
p.add_argument("--input",required=True)
p.add_argument("--output",required=True)
p.add_argument("--k",type=int,default=4)
args=p.parse_args()

spark=SparkSession.builder.appName("customer-kmeans").getOrCreate()
df=spark.read.option("header",True).option("inferSchema",True).csv(args.input)
features=["amount","customer_id"]
pipeline=Pipeline(stages=[
    VectorAssembler(inputCols=features,outputCol="raw_features"),
    StandardScaler(inputCol="raw_features",outputCol="features",withMean=True,withStd=True),
    KMeans(k=args.k,seed=42,featuresCol="features",predictionCol="cluster")
])
model=pipeline.fit(df)
model.transform(df).write.mode("overwrite").parquet(args.output)
spark.stop()
