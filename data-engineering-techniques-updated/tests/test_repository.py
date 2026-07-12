from pathlib import Path
import json
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

def test_required_files():
    required=[
        "README.md","docs/AWS_DEPLOYMENT_RUNBOOK.md","docs/NOTEBOOK_EXECUTION_SEQUENCE.md",
        "config/dataset_contract.yaml",
        "infra/cdk/app.py","infra/cdk/data_engineering_stack.py",
        "scripts/data/generate_customer_behavior.py","scripts/data/validate_dataset.py",
        "scripts/orchestration/create_emr_cluster.py","scripts/orchestration/s3_loader.py",
        "jobs/hadoop/mapper.py","jobs/hadoop/reducer.py",
        "jobs/spark/spark_etl.py","jobs/hive/customer_events.sql",
        "jobs/pig/customer_events.pig","jobs/hbase/customer_events.hbase",
        "jobs/kmeans/spark_kmeans.py",
        "notebooks/07_business_insights_and_visualization.ipynb",
    ]
    for item in required:
        assert (ROOT/item).exists(), item

def test_emr_configuration_json():
    for path in (ROOT/"infra/emr-configurations").glob("*.json"):
        assert isinstance(json.loads(path.read_text()), list)

def test_notebooks_have_code():
    import nbformat
    for path in (ROOT/"notebooks").glob("*.ipynb"):
        nb=nbformat.read(path,as_version=4)
        assert any(c.cell_type=="code" for c in nb.cells)

def test_sample_data_relationships():
    profiles=pd.read_csv(ROOT/"data/sample/customer_profiles.csv")
    events=pd.read_csv(ROOT/"data/sample/customer_events.csv")
    assert profiles.customer_id.is_unique
    assert events.event_id.is_unique
    assert events.customer_id.isin(profiles.customer_id).all()
    assert (events.amount>=0).all()
