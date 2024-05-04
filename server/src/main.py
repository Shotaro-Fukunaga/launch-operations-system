import logging
from http.client import HTTPException
from fastapi import FastAPI, WebSocket, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from src.model import  LaunchCommand
import asyncio
from fastapi import WebSocket, WebSocket, WebSocketDisconnect
import json
from src.settings.config import FLIGHT_PLANS
from src.utils.krpc_module.auto_pilot_manager import FlightManager
import requests
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



@app.get("/flight-plans")
def read_flight_plans():
    """Get all flight plans and event plans stored in the server"""
    # TODO クライアントwebsocketのflightエンドポイントが実行するときに、このエンドポイントからデータを取得する
    return FLIGHT_PLANS.get("flight_plans", [])




@app.websocket("/ws/launch-management")
async def websocket_launch_management(websocket: WebSocket):
    auto_pilot = FlightManager()

    await websocket.accept()

    async def send_telemetry():
        try:
            while True:
                await websocket.send_json(auto_pilot.get_telemetry())
                await asyncio.sleep(0.4)
        except asyncio.CancelledError:
            # タスクがキャンセルされた場合はループを終了
            pass
        except WebSocketDisconnect:
            # WebSocket接続がクライアントによって閉じられた場合
            pass

    telemetry_task = asyncio.create_task(send_telemetry())

    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)  # JSON文字列をPythonの辞書に変換
            command_data = LaunchCommand.model_validate(data)  # Pydanticモデルに変換

            if command_data.command == "disconnect":
                logging.info("Disconnect command received, stopping telemetry and closing connection.")
                break  # ループから抜けてクローズ処理へ

            elif command_data.command == "sequence":
                logging.info(f"Received command: {command_data.target_orbit}")
                auto_pilot.sequence_start(
                    command_data.launch_date,
                    command_data.target_orbit.periapsis,
                    command_data.target_orbit.apoapsis,
                    command_data.target_orbit.inclination,
                    command_data.target_orbit.speed,
                )
    except WebSocketDisconnect:
        logging.info("WebSocket connection has been closed by the client.")
    except asyncio.CancelledError:
        logging.info("WebSocket task was cancelled")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
    finally:
        telemetry_task.cancel()  # テレメトリ送信タスクをキャンセル
        await telemetry_task
        await websocket.close(code=1011, reason="Unexpected error occurred")
        logger.info("WebSocket connection closed")