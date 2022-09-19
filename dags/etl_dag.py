from datetime import datetime
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryGetDatasetOperator,
    BigQueryCreateEmptyDatasetOperator
)
from great_expectations_provider.operators.great_expectations import (
    GreatExpectationsOperator,
)
from packages.stock_data_access.stock_data import _save_stocks_data_to_gbq
from pathlib import Path
import os

DATASET_NAME = 'stocks_storage'
sa_path = os.environ.get('BQ_SERVICE_ACCOUNT_JSON')
BASE_DIR = Path('.').parent.parent.parent.absolute()
GE_ROOT_DIR = Path(BASE_DIR, "great_expectations")
DBT_ROOT_DIR = Path(BASE_DIR, "dbt_transformations")

with DAG(
    "stocks-etl",
    start_date=datetime(2022,8,1),
    schedule_interval="@once",
    catchup=False
    ) as dag:

    upload_stocks_data_to_gbq = PythonOperator(
        task_id = "save_stocks_data_to_gbq",
        python_callable=_save_stocks_data_to_gbq,
        op_args=[['AMZN','FB'],2021,1,1,2022,9,1,sa_path]
    )
    validate_source_stocks_data = GreatExpectationsOperator(
        task_id="validate_source_stocks_data",
        checkpoint_name="stocks_expectations",
        data_context_root_dir=GE_ROOT_DIR,
        fail_task_on_validation_failure=True,
        return_json_dict=True
    )
    run_dbt_dag = BashOperator(
        task_id="run_dbt_dag",
        bash_command=f'cd {DBT_ROOT_DIR} && dbt run'
    )
    test_dbt_dag = BashOperator(
        task_id="test_dbt_dag",
        bash_command=f'cd {DBT_ROOT_DIR} && dbt test'
    )
    Main Stream
    upload_stocks_data_to_gbq
    >> validate_source_stocks_data >> run_dbt_dag >> test_dbt_dag
