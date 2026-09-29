from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}
DBT_DIR = "cd /opt/airflow/sky_audit_dbt"
DBT_FLAGS = "--target container --profiles-dir ."
with DAG(
    dag_id="dbt_build",
    default_args=default_args,
    schedule_interval="30 * * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    dbt_source_freshness = BashOperator(
        task_id="dbt_source_freshness",
        bash_command=f"{DBT_DIR} && dbt source freshness {DBT_FLAGS}"
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=f"{DBT_DIR} && dbt deps --profiles-dir . && dbt build {DBT_FLAGS}",
    )

    dbt_source_freshness >> dbt_build