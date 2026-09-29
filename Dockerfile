FROM apache/airflow:2.9.1

RUN pip install --no-cache-dir \
    kafka-python \
    python-dotenv \
    dbt-core \
    dbt-clickhouse\
    boto3