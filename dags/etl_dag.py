import os
from datetime import datetime
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryGetDatasetOperator,
    BigQueryCreateEmptyDatasetOperator
)

DATASET_NAME = 'stocks_analytics'



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

    get_dataset = BigQueryGetDatasetOperator(task_id="get-dataset", dataset_id=DATASET_NAME)
    On_previous_faild_task = BashOperator(
        task_id = "On_previous_faild_task",
        bash_command="echo 'BigQueryGetDatasetOperator is Faild therefore this Task is running'",
        trigger_rule='all_failed'
    )
    On_previous_success_task = BashOperator(
        task_id = "On_previous_success_task",
        bash_command="echo 'BigQueryGetDatasetOperator is passed successfully!!'",
    )
    create_dataset = BigQueryCreateEmptyDatasetOperator(task_id="create_dataset", dataset_id=DATASET_NAME)
    retry_get_dataset = BigQueryGetDatasetOperator(
        task_id="retry-get-dataset",
        dataset_id=DATASET_NAME,
        trigger_rule='one_success'
    )
    get_dataset_result = BashOperator(
        task_id="get_dataset_result",
        bash_command="echo \"{{ task_instance.xcom_pull('get-dataset')['id'] }}\"",
    )
    get_retry_dataset_result = BashOperator(
        task_id="get_retry_dataset_result",
        bash_command="echo \"{{ task_instance.xcom_pull('retry-get-dataset')['id'] }}\"",
    )
    # Main Stream
    get_dataset >> On_previous_faild_task >> create_dataset >> retry_get_dataset >> get_retry_dataset_result
    get_dataset >> On_previous_success_task >> get_dataset_result
    