import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.settings.router import set_router

# ロギングの基本設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("launch_operations_api")


app = FastAPI(title="LaunchOperationsAPI", version="0.1")


# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


set_router(app)
