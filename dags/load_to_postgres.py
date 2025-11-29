# import snowflake.connector
from display_messages import logging

import psycopg2
import json as json_module


def load_to_postgres(
    PG_USER,
    PG_PASSWORD,
    PG_HOST,
    PG_PORT,
    PG_DB,
    json,
    table_name="raw_data",
    **kwargs,
):
    local_files = kwargs["ti"].xcom_pull(task_ids="download_minio")
    if not local_files:
        logging.error("No files to Load!")
        return

    conn = psycopg2.connect(
        host=PG_HOST, port=PG_PORT, database=PG_DB, user=PG_USER, password=PG_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("SELECT current_database(), current_user;")
    
    logging.info("Successfully connected to postgres!")
    row = cur.fetchone()
    if row:
        db_name, user_name = row
    else:
        db_name, user_name = PG_DB, PG_USER
        logging.warning("Could not fetch current database/user from Postgres; using provided PG_DB/PG_USER")
    logging.info(f"✅ Connected to '{db_name}' as '{user_name}'")
    cur.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            data JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """
    )
    conn.commit()
    for f in local_files:
        with open(f, "r") as file:
            json_data = json_module.load(file)
            cur.execute(
                f"INSERT INTO {table_name} (data) VALUES (%s)", [json_module.dumps(json_data)]
            )
            logging.info(f"Inserted {f} into {table_name}")
        logging.info(f"Uploaded {f} to postgres stage!")
        conn.commit()
    cur.close()
    conn.close()
