from fastapi import APIRouter, HTTPException
from utils.connection import get_connection
from utils.load_env import PG_DB, PG_HOST, PG_PASSWORD, PG_PORT, PG_USER

router = APIRouter()


@router.get("/data_latest")
def get_bronze_data():
    conn = get_connection(PG_HOST, PG_PORT, PG_DB, PG_USER, PG_PASSWORD)
    cur = conn.cursor()
    cur.execute("SELECT *  FROM bronze_stg_stock_quotes")
    return cur.fetchall()
