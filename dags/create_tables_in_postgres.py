import psycopg2


def create_raw_data_table_in_postgres(
    PG_PASSWORD, PG_HOST, PG_PORT, PG_DB, PG_USER, table_name="raw_data"
):
    conn = psycopg2.connect(
        host=PG_HOST, port=PG_PORT, database=PG_DB, user=PG_USER, password=PG_PASSWORD
    )
    cur = conn.cursor()
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
