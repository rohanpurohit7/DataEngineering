# AWS Deployment and Execution Runbook

This runbook takes a new user from an empty AWS account to a working EMR-based data engineering lab.

## What the pipeline solves

The pipeline converts raw customer behavior data into reusable analytical products:

1. **Raw data retention** in Amazon S3.
2. **Distributed cleansing and transformation** with Hadoop and Spark.
3. **SQL-accessible curated tables** with Hive.
4. **Reusable ETL flows** with Pig.
5. **Low-latency customer lookups** with HBase.
6. **Behavioral customer segmentation** with Spark MLlib K-Means.
7. **Operational evidence** through CloudWatch logs and S3 outputs.

The initial business use case is customer behavior analytics. The same architecture can be reused for clickstream, IoT, security logs, financial transactions, healthcare events, or supply-chain telemetry by replacing the dataset contract and job logic.

---

## 1. Prerequisites

Install locally:

```bash
python --version
aws --version
node --version
npm --version
```

Required:

- Python 3.11+
- AWS CLI v2
- Node.js 18+
- AWS CDK v2
- Git
- An AWS account with permission to create VPC, S3, IAM, CloudWatch, and EMR resources

Install CDK:

```bash
npm install -g aws-cdk
cdk --version
```

Configure AWS credentials:

```bash
aws configure
aws sts get-caller-identity
```

Do not store access keys in the repository.

---

## 2. Clone and prepare the repository

```bash
git clone <repository-url>
cd Data-Engineering-Techniques

python -m venv .venv
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

Validate locally:

```bash
pytest -q
python -m compileall scripts jobs infra/cdk
```

---

## 3. Generate or replace seed data

Generate the included customer behavior dataset:

```bash
python scripts/data/generate_customer_behavior.py
```

Outputs:

```text
data/sample/customer_profiles.csv
data/sample/customer_events.csv
```

To use another dataset:

1. Copy the source files into `data/sample/`.
2. Update `config/dataset_contract.yaml`.
3. Update field mappings in the Spark, Hive, Pig, and K-Means jobs.
4. Run `python scripts/data/validate_dataset.py`.
5. Run the notebooks in dry-run mode before AWS deployment.

---

## 4. Deploy network, storage, logging, and IAM

```bash
cd infra/cdk
pip install -r requirements.txt

cdk bootstrap
cdk synth
cdk deploy --outputs-file ../../cdk-outputs.json
cd ../..
```

The stack creates:

- VPC across two Availability Zones
- Public subnets for NAT only
- Private subnets for EMR primary/core/task nodes
- Encrypted and versioned S3 data lake
- EMR service role
- EMR EC2 instance role and instance profile
- CloudWatch log group

Inspect outputs:

```bash
cat cdk-outputs.json
```

The EMR cluster should run in a private subnet. Use S3 for durable storage; use HDFS for temporary distributed processing.

---

## 5. Upload data, scripts, and jobs to S3

Set variables:

```bash
export AWS_REGION=us-east-1
export DATA_BUCKET_NAME=<bucket-from-cdk-output>
```

Upload repository assets:

```bash
python scripts/orchestration/upload_assets.py   --bucket "$DATA_BUCKET_NAME"
```

Verify:

```bash
aws s3 ls "s3://$DATA_BUCKET_NAME/data/raw/" --recursive
aws s3 ls "s3://$DATA_BUCKET_NAME/jobs/" --recursive
aws s3 ls "s3://$DATA_BUCKET_NAME/bootstrap/" --recursive
```

---

## 6. Create the EMR cluster

Identify a private subnet:

```bash
aws ec2 describe-subnets   --filters Name=tag:aws-cdk:subnet-type,Values=Private   --query 'Subnets[0].SubnetId'   --output text
```

Create EMR:

```bash
python scripts/orchestration/create_emr_cluster.py   --bucket "$DATA_BUCKET_NAME"   --subnet-id <private-subnet-id>   --service-role <emr-service-role-name>   --instance-profile DataEngineeringEmrEc2InstanceProfile
```

The script prints the cluster ID.

Monitor:

```bash
aws emr describe-cluster --cluster-id <cluster-id>
aws emr list-instances --cluster-id <cluster-id>
```

Node roles:

- **Primary node:** NameNode, ResourceManager, orchestration
- **Core nodes:** HDFS DataNodes and YARN NodeManagers
- **Task nodes:** scalable compute without HDFS data responsibility

---

## 7. Run notebooks in the intended sequence

Open Jupyter locally:

```bash
jupyter lab
```

Recommended order:

1. `00_aws_emr_orchestration.ipynb`
2. `01_hadoop_mapreduce.ipynb`
3. `02_spark_etl.ipynb`
4. `03_hive_warehouse.ipynb`
5. `04_pig_etl.ipynb`
6. `05_hbase_nosql.ipynb`
7. `06_spark_kmeans.ipynb`
8. `07_business_insights_and_visualization.ipynb`

Each notebook supports:

- `DRY_RUN=true`: prints and validates commands locally
- `DRY_RUN=false`: submits real AWS or cluster work

Set live mode only after validating configuration:

```bash
export DRY_RUN=false
export DATA_BUCKET_NAME=<bucket>
export EMR_CLUSTER_ID=<cluster-id>
```

---

## 8. Load S3 data into notebook execution

Python example:

```python
import boto3
import pandas as pd
from io import BytesIO

bucket = "<bucket>"
key = "data/raw/customer_behavior/customer_profiles.csv"

body = boto3.client("s3").get_object(Bucket=bucket, Key=key)["Body"].read()
profiles = pd.read_csv(BytesIO(body))
profiles.head()
```

PySpark example:

```python
profiles = spark.read.option("header", True).option("inferSchema", True).csv(
    f"s3://{bucket}/data/raw/customer_behavior/customer_profiles.csv"
)
```

Hive example:

```sql
CREATE EXTERNAL TABLE customer_profiles (...)
LOCATION 's3://<bucket>/data/raw/customer_behavior/';
```

---

## 9. Interpret the business outputs

The final analysis notebook answers:

- Which customer groups generate the most revenue?
- Which segments have low engagement or high churn?
- Which regions have high support burden?
- Which event paths indicate purchase intent?
- Which K-Means clusters warrant retention, premium service, or digital engagement campaigns?
- How do event volume and revenue change over time?

The key deliverable is not only a completed job; it is a reusable analytical product stored in the S3 analytics zone.

---

## 10. Scale the platform

For larger datasets:

- Convert CSV to partitioned Parquet.
- Partition by date and high-value business dimensions.
- Increase core nodes for HDFS-heavy processing.
- Add task nodes for elastic Spark/YARN compute.
- Use EMR Managed Scaling.
- Use Spot task nodes only for interruption-tolerant work.
- Compact small files.
- Enable Spark adaptive query execution.
- Persist reusable curated tables in S3, not HDFS.
- Use Glue Data Catalog if multiple consumers need shared metadata.
- Separate dev, test, and production AWS accounts.

---

## 11. Reuse with another dataset

Use this checklist:

1. Define a business decision.
2. Add a dataset contract.
3. Add raw data to S3.
4. Validate schema and quality.
5. Update transformations.
6. Update Hive table definitions.
7. Update feature assembly for ML jobs.
8. Update charts and KPI definitions.
9. Execute in dry-run mode.
10. Deploy and run on EMR.
11. Store curated and analytics outputs in S3.
12. Document lineage and operating assumptions.

---

## 12. Shut down and control cost

Terminate the cluster:

```bash
aws emr terminate-clusters --cluster-ids <cluster-id>
```

Destroy CDK resources:

```bash
cd infra/cdk
cdk destroy
```

Review retained S3 objects manually before deleting the bucket.
