import logging

from fastapi import APIRouter, Depends, WebSocket, WebSocket, WebSocketDisconnect

from src.settings.database import get_db
from src.utils.krpc_module.rocket_telemetry import RocketTelemetry
from src.utils.websocket_handler import common_websocket_handler

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ws")

rocket = RocketTelemetry("web_socket_server")


@router.websocket("/atmosphere_info")
async def websocket_atmosphere_info(websocket: WebSocket):
    await common_websocket_handler(websocket, rocket.get_atmosphere_info)


@router.websocket("/orbit_info")
async def websocket_orbit_info(websocket: WebSocket):
    await common_websocket_handler(websocket, rocket.get_orbit_info)


@router.websocket("/surface_info")
async def websocket_surface_info(websocket: WebSocket):
    await common_websocket_handler(websocket, rocket.get_surface_info)


@router.websocket("/delta_v_status")
async def websocket_delta_v_status(websocket: WebSocket):
    await common_websocket_handler(websocket, rocket.get_delta_v_status)


@router.websocket("/thermal_status")
async def websocket_thermal_status(websocket: WebSocket):
    await common_websocket_handler(websocket, rocket.get_thermal_status)


@router.websocket("/satellite_bus_status")
async def satellite_bus_status(websocket: WebSocket):
    await common_websocket_handler(websocket, rocket.get_satellite_bus_status)


@router.websocket("/communication_status")
async def communication_status(websocket: WebSocket):
    await common_websocket_handler(websocket, rocket.get_communication_status)
