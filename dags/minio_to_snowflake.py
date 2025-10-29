import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from dotenv import load_dotenv
from download_from_minio import download_from_minio
from load_to_snowflake import load_to_snowflake

# Load environment variables
load_dotenv()

MINIO_ENDPOINT = "http://minio:9000"
LOCAL_DIR = "/tmp/minio_downloads"
BUCKET = "bronze-transactions"

MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")

SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DB = os.getenv("SNOWFLAKE_DB")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 10, 14),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="minio_to_snowflake",
    default_args=default_args,
    schedule="@hourly",
    catchup=False,
) as dag:

    download_task = PythonOperator(
        task_id="download_minio",
        python_callable=download_from_minio,
        op_kwargs={
            "LOCAL_DIR": LOCAL_DIR,
            "MINIO_ENDPOINT": MINIO_ENDPOINT,
            "MINIO_ACCESS_KEY": MINIO_ACCESS_KEY,
            "MINIO_SECRET_KEY": MINIO_SECRET_KEY,
            "BUCKET": BUCKET,
        },
    )

    load_task = PythonOperator(
        task_id="load_snowflake",
        python_callable=load_to_snowflake,
        provide_context=True,
        op_kwargs={
            "SNOWFLAKE_USER": SNOWFLAKE_USER,
            "SNOWFLAKE_ACCOUNT": SNOWFLAKE_ACCOUNT,
            "SNOWFLAKE_WAREHOUSE": SNOWFLAKE_WAREHOUSE,
            "SNOWFLAKE_DB": SNOWFLAKE_DB,
            "SNOWFLAKE_SCHEMA": SNOWFLAKE_SCHEMA,
            "SNOWFLAKE_PASSWORD": SNOWFLAKE_PASSWORD,
        },
    )

    download_task >> load_task
