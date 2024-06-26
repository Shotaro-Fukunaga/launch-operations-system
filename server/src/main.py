"""LaunchOperationsAPI FastAPI application."""

import asyncio
import json
import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from src.model import LaunchCommand
from src.utils.krpc_module.auto_pilot_manager import FlightManager
from src.utils.krpc_module.krpc_client import KrpcClient

app = FastAPI(title="LaunchOperationsAPI", version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)
krpc = KrpcClient("MyKSPConnection")


@app.websocket("/ws/launch-management")
async def websocket_launch_management(websocket: WebSocket) -> None:
    """Manage the launch process through WebSocket communication."""
    auto_pilot = FlightManager(krpc)
    await websocket.accept()

    telemetry_task = asyncio.create_task(send_telemetry(websocket, auto_pilot))
    commands_task = asyncio.create_task(receive_commands(websocket, auto_pilot))

    done, pending = await asyncio.wait(
        [telemetry_task, commands_task],
        return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            logger.info("Cancelled pending task")

        # Clean up the FlightManager instance
    await auto_pilot.close()


async def send_telemetry(websocket: WebSocket, auto_pilot: FlightManager) -> None:
    """Send telemetry data periodically to the connected client."""
    try:
        while True:
            await websocket.send_json(await auto_pilot.get_telemetry())
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed by client.")
    except Exception:
        logger.exception("Error sending telemetry")
        raise


async def receive_commands(websocket: WebSocket, auto_pilot: FlightManager) -> None:
    """Receive and handle commands from the connected client."""
    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)
            command_data = LaunchCommand.model_validate(data)

            if command_data.command == "disconnect":
                logger.info("Disconnect command received, closing connection.")
                await websocket.close()
                break
            await execute_command(command_data, auto_pilot)
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed by client.")
    except asyncio.CancelledError:
        logger.info("WebSocket task was cancelled")
    except Exception:
        logger.exception("An unexpected error occurred")
        await websocket.close(code=1011, reason="Unexpected error occurred")
        logger.info("WebSocket connection closed")
        raise


async def execute_command(command_data: LaunchCommand, auto_pilot: FlightManager) -> None:
    """Execute a received command based on the command type."""
    if command_data.command == "sequence":
        logger.info("Received sequence command for: %s", command_data.launch_date)
        await auto_pilot.sequence_start(command_data)
