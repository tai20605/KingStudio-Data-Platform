"""Check that every DAG in airflow/dags imports without errors."""

from pathlib import Path

try:
    from airflow.dag_processing.dagbag import DagBag
except ImportError:  # older Airflow 3 releases
    from airflow.models import DagBag

DAG_FOLDER = Path(__file__).resolve().parents[2] / "airflow" / "dags"


def test_no_import_errors():
    dag_bag = DagBag(dag_folder=str(DAG_FOLDER), include_examples=False)
    assert not dag_bag.import_errors, f"DAG import errors: {dag_bag.import_errors}"
