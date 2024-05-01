import logging
import asyncio
from fastapi import FastAPI, WebSocket, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from src.config import base_rocket, EVENT_PLANS, FLIGHT_PLANS
from src.utils.websocket_handler import common_websocket_handler
from src.utils.krpc_module.record_manager import RecordManager
from src.utils.krpc_module.rocket_telemetry import RocketTelemetry

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



flight_manager = RecordManager(base_rocket)
rocket = RocketTelemetry(base_rocket)


@app.post("/flight/launch-sequence")
def launch_sequence():
    return flight_manager.launch_sequence()


@app.get("/flight-plans")
def read_flight_plans():
    """Get all flight plans and event plans stored in the server"""
    # TODO クライアントwebsocketのflightエンドポイントが実行するときに、このエンドポイントからデータを取得する
    return {"flight_plans": FLIGHT_PLANS.get("flight_plans", []), "event_plans": EVENT_PLANS.get("event_plans", [])}


@app.get("/get_telemetry_data")
def get_telemetry_data():
    return rocket.get_telemetry_data()


@app.get("/get_rocket_data")
def get_rocket_data():
    return rocket.get_rocket_data()


@app.get("/flight/records")
def get_flight_records():
    return flight_manager.get_records()


@app.websocket("/ws/chart-telemetry")
async def websocket_dashboard_telemetry(websocket: WebSocket):
    await common_websocket_handler(websocket, rocket.get_telemetry_data)


@app.websocket("/ws/rocket-status")
async def websocket_rocket_status(websocket: WebSocket):
    await asyncio.sleep(1)  # 接続が安定するまで少し待つ
    await common_websocket_handler(websocket, rocket.get_rocket_data)

@app.websocket("/ws/rocket-record")
async def websocket_rocket_status(websocket: WebSocket):
    await common_websocket_handler(websocket, flight_manager.get_records)
