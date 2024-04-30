import asyncio
import logging

from fastapi import APIRouter, WebSocket, WebSocket, WebSocketDisconnect
from src.utils.krpc_module.rocket_telemetry import RocketTelemetry
from src.utils.krpc_module.flight_manager import FlightManager
from src.utils.krpc_module.rocket_event import EventManager
from src.settings.config import base_rocket
from src.utils.websocket_handler import common_websocket_handler
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ws")

rocket = RocketTelemetry(base_rocket)


@router.websocket("/flight-manager/{flight_id}")
async def websocket_flight_manager(
    websocket: WebSocket,
    flight_id: int,
):
    launch_datetime = datetime.now(timezone.utc) + timedelta(seconds=10)
    target_periapsis = 200000
    target_apoapsis = 200000
    target_orbit_inc = 30.39
    flight_id = 121
    max_q_altitude = 11200
    target_orbit_speed = 7788

    manager_config = {
        "rocket_core": base_rocket,
        "launch_datetime": launch_datetime,
        "target_periapsis": target_periapsis,
        "target_apoapsis": target_apoapsis,
        "target_orbit_inc": target_orbit_inc,
        "flight_id": flight_id,
        "max_q_altitude": max_q_altitude,
        "target_orbit_speed": target_orbit_speed,
    }

    # 辞書を展開して各マネージャーを初期化
    flight_manager = FlightManager(**manager_config)
    event_manager = EventManager(**manager_config)

    await websocket.accept()

    # フライトシーケンスの開始
    flight_manager.launch_sequence()

    # メインループ: ミッション完了までデータ送信
    try:
        while not flight_manager.mission_complete:
            event_manager.event_update()
            data = {"flight_records": flight_manager.get_flight_records(), "event_records": event_manager.get_events()}
            await websocket.send_json(data)
            await asyncio.sleep(1)

        # ミッション完了時の処理
        event_manager.record_event_data("Mission complete", "Mission has been completed", is_significant=True)
        event_manager.save_event_records()
        await websocket.close(code=1000, reason="Mission complete")

    # エラーハンドリング
    except WebSocketDisconnect:
        logging.info("WebSocket connection has been closed by the client.")
    except asyncio.CancelledError:
        logging.info("WebSocket task was cancelled")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        await websocket.close(code=1011, reason="Unexpected error occurred")


@router.websocket("/dashboard-telemetry")
async def websocket_dashboard_telemetry(websocket: WebSocket):
    await common_websocket_handler(websocket, rocket.get_telemetry_data)



@router.websocket("/rocket-status")
async def websocket_rocket_status(websocket: WebSocket):
    await common_websocket_handler(websocket, rocket.get_rocket_data)
