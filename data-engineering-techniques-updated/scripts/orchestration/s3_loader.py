from __future__ import annotations
from io import BytesIO
from pathlib import Path
import os
import boto3
import pandas as pd

def load_csv(bucket: str, key: str, parse_dates: list[str] | None = None) -> pd.DataFrame:
    body = boto3.client("s3").get_object(Bucket=bucket, Key=key)["Body"].read()
    return pd.read_csv(BytesIO(body), parse_dates=parse_dates)

def load_dataset(
    local_path: str | Path,
    s3_key: str,
    parse_dates: list[str] | None = None,
) -> pd.DataFrame:
    bucket = os.getenv("DATA_BUCKET_NAME")
    use_s3 = os.getenv("USE_S3", "false").lower() == "true"
    if use_s3:
        if not bucket:
            raise RuntimeError("DATA_BUCKET_NAME is required when USE_S3=true")
        print(f"Loading s3://{bucket}/{s3_key}")
        return load_csv(bucket, s3_key, parse_dates=parse_dates)
    print(f"Loading local file: {local_path}")
    return pd.read_csv(local_path, parse_dates=parse_dates)
