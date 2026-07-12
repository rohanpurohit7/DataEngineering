from pyspark.sql import SparkSession, functions as F
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.clustering import KMeans
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import ClusteringEvaluator
import argparse

p=argparse.ArgumentParser()
p.add_argument("--input",required=True)
p.add_argument("--output",required=True)
p.add_argument("--k",type=int,default=4)
args=p.parse_args()

spark=SparkSession.builder.appName("customer-behavior-kmeans").getOrCreate()
df=spark.read.option("header",True).option("inferSchema",True).csv(args.input)

features=[
    "monthly_income","tenure_months","digital_logins_30d",
    "purchase_frequency_30d","avg_order_value",
    "support_calls_90d","returns_90d","engagement_score"
]

pipeline=Pipeline(stages=[
    VectorAssembler(inputCols=features,outputCol="raw_features"),
    StandardScaler(inputCol="raw_features",outputCol="features",withMean=True,withStd=True),
    KMeans(k=args.k,seed=42,featuresCol="features",predictionCol="cluster")
])

model=pipeline.fit(df)
pred=model.transform(df)
score=ClusteringEvaluator(featuresCol="features",predictionCol="cluster").evaluate(pred)
print(f"silhouette_score={score}")

profile=(pred.groupBy("cluster")
         .agg(F.count("*").alias("customers"),
              F.avg("engagement_score").alias("avg_engagement"),
              F.avg("purchase_frequency_30d").alias("avg_purchase_frequency"),
              F.avg("avg_order_value").alias("avg_order_value"),
              F.avg("support_calls_90d").alias("avg_support_calls"),
              F.avg("churned").alias("churn_rate")))
profile.show(truncate=False)

pred.drop("raw_features","features").write.mode("overwrite").parquet(args.output)
profile.write.mode("overwrite").json(args.output.rstrip("/")+"_profiles")
spark.stop()
