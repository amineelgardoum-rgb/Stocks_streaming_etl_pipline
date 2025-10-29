def create_dags(
    DAG, PythonOperator, download_from_minio, load_to_snowflake, default_args
):
    with DAG(
        dag_id="minio_to_snowflake",
        default_args=default_args,
        schedule="* * * * *",
        catchup=False,
    ) as dag:
        task1 = PythonOperator(
            task_id="download_minio", python_callable=download_from_minio
        )
        task2 = PythonOperator(
            task_id="load_snowflake",
            python_callable=load_to_snowflake,
            provide_context=True,
        )
        task1 >> task2
    return dag
