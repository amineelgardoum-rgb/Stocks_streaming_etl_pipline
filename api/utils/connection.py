import psycopg2 as ps
from psycopg2.extras import RealDictCursor


def get_connection(PG_HOST, PG_PORT, PG_DB, PG_USER, PG_PASSWORD):
    return ps.connect(
        host=PG_HOST,
        port=PG_PORT,
        database=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD,
        cursor_factory=RealDictCursor,
    )
