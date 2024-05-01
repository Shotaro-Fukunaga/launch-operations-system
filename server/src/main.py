import logging
from http.client import HTTPException
from fastapi import FastAPI, WebSocket, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from src.model import LaunchParameters
from src.utils.krpc_module.krpc_client import KrpcClient
from src.utils.krpc_module.vessel_manager import VesselManager
from src.settings.config import FLIGHT_PLANS, rocket_schema_list
from src.utils.websocket_handler import common_websocket_handler
from src.utils.krpc_module.auto_pilot_manager import AutoPilotManager

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

krpc_client = KrpcClient("LaunchOperationsAPI")
vessel_manager = VesselManager(krpc_client.client, rocket_schema_list)


@app.get("/flight-plans")
def read_flight_plans():
    """Get all flight plans and event plans stored in the server"""
    # TODO クライアントwebsocketのflightエンドポイントが実行するときに、このエンドポイントからデータを取得する
    return FLIGHT_PLANS.get("flight_plans", [])


@app.post("/start-launch-sequence")
def start_launch_sequence(body: LaunchParameters):
    if not krpc_client.is_connected:
        raise HTTPException(status_code=503, detail="KRPC server is not connected.")
    auto_pilot = AutoPilotManager(vessel_manager)
    return auto_pilot.launch_sequence(**body.model_dump())


@app.get("/get-vessel-telemetry")
def get_telemetry():
    if not krpc_client.is_connected:
        raise HTTPException(status_code=503, detail="KRPC server is not connected.")
    return vessel_manager.get_vessel_telemetry()


@app.get("/get-rocket-status")
def get_rocket_status():
    if not krpc_client.is_connected:
        raise HTTPException(status_code=503, detail="KRPC server is not connected.")
    return vessel_manager.get_rocket_status()


@app.get("/get-flight-records")
def get_flight_records():
    if not krpc_client.is_connected:
        raise HTTPException(status_code=503, detail="KRPC server is not connected.")
    return vessel_manager.get_flight_records()


@app.websocket("/ws/vessel-telemetry")
async def websocket_vessel_telemetry(websocket: WebSocket):
    if not krpc_client.is_connected:
        await websocket.close(code=1011, reason="KRPC server is not connected.")
        return
    await common_websocket_handler(websocket, vessel_manager.get_vessel_telemetry)


@app.websocket("/ws/rocket-status")
async def websocket_rocket_status(websocket: WebSocket):
    if not krpc_client.is_connected:
        await websocket.close(code=1011, reason="KRPC server is not connected.")
        return
    await common_websocket_handler(websocket, vessel_manager.get_rocket_status)


@app.websocket("/ws/flight-records")
async def websocket_flight_records(websocket: WebSocket):
    if not krpc_client.is_connected:
        await websocket.close(code=1011, reason="KRPC server is not connected.")
        return
    await common_websocket_handler(websocket, vessel_manager.get_flight_records)
