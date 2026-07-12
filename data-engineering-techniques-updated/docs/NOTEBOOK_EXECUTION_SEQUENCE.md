# Notebook Execution Sequence

| Order | Notebook | Purpose | Main output |
|---:|---|---|---|
| 1 | `00_aws_emr_orchestration.ipynb` | Validate environment and deployment commands | AWS deployment plan |
| 2 | `01_hadoop_mapreduce.ipynb` | Demonstrate distributed map/reduce counting | Event counts |
| 3 | `02_spark_etl.ipynb` | Transform raw events into curated Parquet | Partitioned curated data |
| 4 | `03_hive_warehouse.ipynb` | Create queryable analytical tables | Hive summaries |
| 5 | `04_pig_etl.ipynb` | Run declarative ETL | Aggregated event output |
| 6 | `05_hbase_nosql.ipynb` | Demonstrate low-latency record access | HBase table |
| 7 | `06_spark_kmeans.ipynb` | Produce distributed customer clusters | Cluster assignments and profiles |
| 8 | `07_business_insights_and_visualization.ipynb` | Interpret pipeline outputs | KPIs, charts, segment recommendations |

Use `USE_S3=false` for local files. Use `USE_S3=true` and `DATA_BUCKET_NAME=<bucket>` to load from S3.
