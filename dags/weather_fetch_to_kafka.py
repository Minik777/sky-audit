from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    "execution_timeout": timedelta(minutes=5),
}

with DAG(
    dag_id="weather_fetch_to_kafka",
    default_args=default_args,
    schedule_interval="0 * * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    load_raw_data_to_minio = BashOperator(
        task_id="load_raw_data_to_minio",
        bash_command="cd /opt/airflow/src && python load_from.py {{ ts_nodash }}",
    )

    get_from_minio_and_producer = BashOperator(
        task_id = "get_from_minio_and_producer",
        bash_command="cd /opt/airflow/src && python producer.py {{ ts_nodash }}",

    )

load_raw_data_to_minio >> get_from_minio_and_producer