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
import os

DATASET_NAME = 'stocks_storage'
sa_path = os.environ.get('SERVICE_ACCOUNT_JSON_PATH')
GE_ROOT_DIR = os.getcwd() + "/great_expectations"

with DAG(
    "stocks-etl",
    start_date=datetime(2022,8,1),
    schedule_interval="@once",
    catchup=False
    ) as dag:
    # TODO: Check the exsistance of the dataset using get_dataset operator and branch operator
    # If it's not exists create a new dataset with an operator
    # if it's exists check if the table exists or not using a branch operator again:
                # if it's not exists create the table then che
                # if it's exists  
    upload_stocks_data_to_gbq = PythonOperator(
        task_id = "save_stocks_data_to_gbq",
        python_callable=_save_stocks_data_to_gbq,
        op_args=['AMZN',2022,1,1,2022,2,1,sa_path]
    )
    validate_stocks_data = GreatExpectationsOperator(
        task_id="validate_stocks_data",
        checkpoint_name="stocks_expectations",
        data_context_root_dir=GE_ROOT_DIR,
        fail_task_on_validation_failure=True,
        return_json_dict=True
    )
    # Main Stream
    upload_stocks_data_to_gbq >> validate_stocks_data
