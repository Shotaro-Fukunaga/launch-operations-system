
import logging

from fastapi import APIRouter
# from src.settings.database import get_db
from src.utils.krpc_module.rocket_telemetry import RocketTelemetry

from src.settings.config import ROCKET_SCHEMAS
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/{version}/flight",
    tags=["Flight"],
)

rocket = RocketTelemetry("http_server",ROCKET_SCHEMAS)



@router.get("/get_atmosphere_info")
def get_atmosphere_info():
    return rocket.get_atmosphere_info()

@router.get("/get_orbit_info")
def get_orbit_info():
    return rocket.get_orbit_info()

@router.get("/get_surface_info")
def get_surface_info():
    return rocket.get_surface_info()

@router.get("/get_delta_v_status")
def get_delta_v_status():
    return rocket.get_delta_v_status()

@router.get("/get_fuel_status")
def get_fuel_status():
    return rocket.get_fuel_status()

@router.get("/get_thermal_status")
def get_thermal_status():
    return rocket.get_thermal_status()


@router.get("/get_payload_status")
def get_payload_status():
    return rocket.get_payload_status()


@router.get("/get_communication_status")
def get_communication_status():
    return rocket.get_communication_status()

# TODO ロケットの予定イベント情報を返却するエンドポイントの実装
# ここに予定軌道情報も含めて返すようにする
# export type EventType = {
# time: string
# name: string
# color?: string;
# status: "success" | "warning" | "error" | "info"
# }


# TODO ロケットの実際のイベント情報を返却するエンドポイントの実装
# ここに実際の軌道情報も含めて返すようにする


