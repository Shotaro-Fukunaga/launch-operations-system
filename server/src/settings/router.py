from fastapi import Depends, FastAPI
from src.api.flights.router import router as flight_router

def set_router(app: FastAPI) -> None:
    """ルーティングのセットアップ関数

    Args:
        app (FastAPI): _description_
    """
    app.include_router(flight_router)