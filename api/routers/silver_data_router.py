from fastapi import APIRouter
from utils.connection import get_connection

from utils.load_env import PG_DB, PG_HOST, PG_PASSWORD, PG_PORT, PG_USER

router = APIRouter()


@router.get("/silver_data")
def get_sliver_data():
    conn = get_connection(PG_HOST, PG_PORT, PG_DB, PG_USER, PG_PASSWORD)
    cur = conn.cursor()
    cur.execute("SELECT *  FROM silver_clean_stock_quotes")
    return cur.fetchall()
