import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from dotenv import load_dotenv
from download_from_minio import download_from_minio
from load_to_postgres import load_to_postgres
import json

# Load environment variables
load_dotenv()

MINIO_ENDPOINT = "http://minio:9000"
LOCAL_DIR = "/tmp/minio_downloads"
BUCKET = "bronze-transactions"

MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")

PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DB = os.getenv("PG_DB")

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 10, 14),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="minio_to_postgres",
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
        task_id="load_postgres",
        python_callable=load_to_postgres,
        provide_context=True,
        op_kwargs={
            "PG_USER": PG_USER,
            "PG_PASSWORD": PG_PASSWORD,
            "PG_HOST": PG_HOST,
            "PG_PORT": PG_PORT,
            "PG_DB": PG_DB,
            "json": json,
            "table_name": "raw_data",
        },
    )

    download_task >> load_task
