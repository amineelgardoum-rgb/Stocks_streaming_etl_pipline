from routers import init_router,gold_candlestick_data_router,gold_treechart_data_router,silver_data_router
from fastapi import FastAPI
app=FastAPI()
app.include_router(init_router.router)
app.include_router(silver_data_router.router,prefix="/silver")
app.include_router(gold_candlestick_data_router.router,prefix="/gold/candlestick")
app.include_router(gold_treechart_data_router.router,prefix="/gold/treechart")
