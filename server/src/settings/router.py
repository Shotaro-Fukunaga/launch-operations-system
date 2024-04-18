from fastapi import FastAPI
from src.routers.http_router import router as http_flight_router
from src.routers.web_socket_router import router as web_socket_router

def set_router(app: FastAPI) -> None:
    """ルーティングのセットアップ関数

    Args:
        app (FastAPI): _description_
    """
    app.include_router(http_flight_router)
    app.include_router(web_socket_router)