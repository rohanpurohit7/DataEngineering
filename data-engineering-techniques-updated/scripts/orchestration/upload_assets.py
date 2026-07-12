from __future__ import annotations
import argparse
from pathlib import Path
import boto3

ROOT = Path(__file__).resolve().parents[2]

def upload_tree(bucket: str, source: Path, prefix: str) -> None:
    s3 = boto3.client("s3")
    for path in source.rglob("*"):
        if path.is_file():
            key = f"{prefix}/{path.relative_to(source).as_posix()}"
            print(f"upload {path} -> s3://{bucket}/{key}")
            s3.upload_file(str(path), bucket, key)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", required=True)
    args = parser.parse_args()
    upload_tree(args.bucket, ROOT / "jobs", "jobs")
    upload_tree(args.bucket, ROOT / "scripts/bootstrap", "bootstrap")
    upload_tree(args.bucket, ROOT / "data/sample", "data/raw/customer_behavior")
    upload_tree(args.bucket, ROOT / "config", "config")

if __name__ == "__main__":
    main()
