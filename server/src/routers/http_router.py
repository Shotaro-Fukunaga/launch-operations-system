import logging

from fastapi import APIRouter, Depends, HTTPException

from src.utils.krpc_module.flight_manager import FlightManager
from src.utils.krpc_module.rocket_event import EventManager
from src.utils.krpc_module.rocket_telemetry import RocketTelemetry
from src.settings.config import base_rocket, EVENT_PLANS, FLIGHT_PLANS
from datetime import datetime, timedelta,timezone

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/{version}/flight",
    tags=["Flight"],
)


rocket = RocketTelemetry(base_rocket)


@router.get("/flight-plans")
def read_flight_plans():
    """Get all flight plans and event plans stored in the server"""
    # TODO クライアントwebsocketのflightエンドポイントが実行するときに、このエンドポイントからデータを取得する
    return {"flight_plans": FLIGHT_PLANS.get("flight_plans", []), "event_plans": EVENT_PLANS.get("event_plans", [])}


# 確認用のエンドポイント


# @router.get("/flight-manager/{flight_id}")
# async def get_flight_status(flight_id: int):
#     launch_datetime = datetime.now(timezone.utc) + timedelta(seconds=10)
#     target_periapsis = 200000
#     target_apoapsis = 200000
#     target_orbit_inc = 30.39
#     flight_id = 121
#     max_q_altitude = 11200
#     target_orbit_speed = 7788

#     manager_config = {
#         "rocket_core": base_rocket,
#         "launch_datetime": launch_datetime,
#         "target_periapsis": target_periapsis,
#         "target_apoapsis": target_apoapsis,
#         "target_orbit_inc": target_orbit_inc,
#         "flight_id": flight_id,
#         "max_q_altitude": max_q_altitude,
#         "target_orbit_speed": target_orbit_speed,
#     }

#     flight_manager = FlightManager(**manager_config)
#     event_manager = EventManager(**manager_config)

#     # フライトシーケンスの開始（一度だけ実行するための条件が必要かもしれません）
#     flight_manager.launch_sequence()

#     if flight_manager.mission_complete:
#         # ミッションが完了している場合
#         return {"status": "completed", "details": "Mission has been completed"}

#     # イベント更新とフライトレコードの取得
#     event_manager.event_update()
#     data = {"flight_records": flight_manager.get_flight_records(), "event_records": event_manager.get_events()}

#     return data


# @router.get("/get_atmosphere_info")
# def get_atmosphere_info():
#     return rocket.get_atmosphere_info()


# @router.get("/get_orbit_info")
# def get_orbit_info():
#     return rocket.get_orbit_info()


# @router.get("/get_surface_info")
# def get_surface_info():
#     return rocket.get_surface_info()


# @router.get("/get_delta_v_status")
# def get_delta_v_status():
#     return rocket.get_delta_v_status()


# @router.get("/get_fuel_status")
# def get_fuel_status():
#     return rocket.get_fuel_status()


# @router.get("/get_thermal_status")
# def get_thermal_status():
#     return rocket.get_thermal_status()


# @router.get("/get_payload_status")
# def get_payload_status():
#     return rocket.get_payload_status()


# @router.get("/get_communication_status")
# def get_communication_status():
#     return rocket.get_communication_status()

# @router.get("/get_telemetry_data")
# def get_telemetry_data():
#     return rocket.get_telemetry_data()

# @router.get("/get_rocket_data")
# def get_rocket_data():
#     return rocket.get_rocket_data()
