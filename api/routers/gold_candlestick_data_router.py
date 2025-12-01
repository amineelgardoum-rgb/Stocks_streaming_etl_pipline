from fastapi import APIRouter, HTTPException
from utils.connection import get_connection
from utils.load_env import PG_DB, PG_HOST, PG_PASSWORD, PG_PORT, PG_USER

router = APIRouter()


@router.get("/gold_candlestick_data")
def get_gold_candlestick_data():
    conn = get_connection(PG_HOST, PG_PORT, PG_DB, PG_USER, PG_PASSWORD)
    cur = conn.cursor()
    cur.execute("select * FROM gold_candlestick;")
    return cur.fetchall()
