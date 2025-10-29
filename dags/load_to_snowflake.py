import snowflake.connector
from display_messages import logging


def load_to_snowflake(
    SNOWFLAKE_USER,
    SNOWFLAKE_ACCOUNT,
    SNOWFLAKE_WAREHOUSE,
    SNOWFLAKE_DB,
    SNOWFLAKE_SCHEMA,
    SNOWFLAKE_PASSWORD,
    **kwargs,
):
    local_files = kwargs["ti"].xcom_pull(task_ids="download_minio")
    if not local_files:
        logging.error("No files to Load!")
        return

    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DB,
        schema=SNOWFLAKE_SCHEMA,
    )
    cur = conn.cursor()
    for f in local_files:
        cur.execute(f"PUT file://{f} @%BRONZE_STOCKS_QUOTES_RAW")
        logging.info(f"Uploaded {f} to Snowflake stage!")

    cur.execute(
        """
                COPY INTO BRONZE_STOCKS_QUOTES_RAW
                FROM @%BRONZE_STOCKS_QUOTES_RAW
                FILE_FORMAT=(TYPE=JSON)
                """
    )
    logging.info("COPY INTO executed")
    cur.close()
    conn.close()
