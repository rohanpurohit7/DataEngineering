from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def test_required_files():
    required=[
        "README.md","infra/cdk/app.py","infra/cdk/data_engineering_stack.py",
        "scripts/orchestration/create_emr_cluster.py",
        "jobs/hadoop/mapper.py","jobs/hadoop/reducer.py",
        "jobs/spark/spark_etl.py","jobs/hive/customer_events.sql",
        "jobs/pig/customer_events.pig","jobs/hbase/customer_events.hbase",
        "jobs/kmeans/spark_kmeans.py",
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
