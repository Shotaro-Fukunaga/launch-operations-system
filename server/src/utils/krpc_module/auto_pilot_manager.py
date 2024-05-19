import asyncio
import logging
import math
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from krpc.services.spacecenter import SASMode

from src.model import LaunchCommand
from src.settings.config import FLIGHT_LOG_FILE_PATH, GO, ROCKET_SCHEMAS
from src.utils.commons.log_manager import LogManager
from src.utils.krpc_module.krpc_client import KrpcClient
from src.utils.krpc_module.rocket_status_manager import RocketStatusManager
from src.utils.krpc_module.telemetry_manager import TelemetryManager
from src.utils.krpc_module.vessel_manager import VesselManager

logger = logging.getLogger(__name__)
LAUNCH_WARNING_THRESHOLD = -5


class FlightManager:
    """ロケットの飛行を管理するクラス"""

    def __init__(self: "FlightManager", krpc: KrpcClient) -> None:
        """Initialize the FlightManager class."""
        if krpc.client is None:
            msg = "KRPC client is not available."
            raise ValueError(msg)
        self.vessel_manager = VesselManager(krpc.client, ROCKET_SCHEMAS)
        self.telemetry_manager = TelemetryManager(self.vessel_manager)
        self.launch_relative_time = 0
        self.status_manager = RocketStatusManager(self)
        self.log_file_path = Path(FLIGHT_LOG_FILE_PATH)
        self.executor = ThreadPoolExecutor()

    async def close(self: "FlightManager") -> None:
        """クリーンアップ処理を実行する"""
        self.executor.shutdown(wait=True)
        # 必要に応じて他のクリーンアップ処理を追加する

    async def countdown_and_countup(self: "FlightManager", launch_date: datetime) -> None:
        """カウントダウンとカウントアップを開始する"""
        target_time = time.perf_counter()
        while True:
            now = datetime.now(timezone.utc)
            time_diff = now - launch_date
            self.launch_relative_time = math.floor(time_diff.total_seconds())

            # フライトデータの記録
            data = self.flight_record_data()
            if data:
                await LogManager.save_to_log_async(data, self.log_file_path)

            # 次のループの目標時間を計算
            target_time += 1.0
            sleep_time = max(0, target_time - time.perf_counter())

            await asyncio.sleep(sleep_time)

    async def sequence_start(
        self: "FlightManager",
        command_data: LaunchCommand,
        max_q_altitude: int = 11200,
    ) -> None:
        """ロケットの打ち上げシーケンスを開始する"""
        # ユニットを初期化
        self.vessel_manager.set_all_units_status(GO)
        # カウントダウンとカウントアップを開始
        countdown_task = asyncio.create_task(self.countdown_and_countup(command_data.launch_date))

        try:
            # 打ち上げ時刻まで待機
            while True:
                if LAUNCH_WARNING_THRESHOLD <= self.launch_relative_time <= 0:
                    self.add_event_log(f"Launch in T{self.launch_relative_time} seconds")
                if self.launch_relative_time > 0:
                    self.add_event_log(
                        f"Launch countdown complete: T+{self.launch_relative_time} seconds",
                    )
                    break
                await asyncio.sleep(1)

            # オートパイロットを開始
            await self.execute_autopilot(
                command_data,
                max_q_altitude,
            )
        finally:
            countdown_task.cancel()

    async def execute_autopilot(
        self: "FlightManager",
        command_data: LaunchCommand,
        max_q_altitude: int,
    ) -> None:
        """オートパイロットを実行する"""
        vessel = self.vessel_manager.vessel
        mechjeb = self.vessel_manager.mech_jeb
        target = command_data.target_orbit

        # Get the ascent autopilot module
        ascent_autopilot = mechjeb.ascent_autopilot
        ascent_path_guidance = ascent_autopilot.ascent_path_pvg
        ascent_autopilot.ascent_path_index = 2
        # Configure autopilot settings
        ascent_autopilot.desired_orbit_altitude = target.periapsis
        ascent_autopilot.desired_inclination = target.inclination
        ascent_path_guidance.desired_apoapsis = target.apoapsis
        ascent_autopilot.force_roll = True
        ascent_autopilot.turn_roll = 90
        ascent_autopilot.autodeploy_solar_panels = True
        ascent_autopilot.auto_deploy_antennas = True
        ascent_autopilot.autostage = True
        ascent_autopilot.enabled = True

        await self.activate_next_stage_async()
        logger.info("Rocket Lift off - Stage activated")

        max_q_passed = False
        try:
            while ascent_autopilot.enabled:
                if self.vessel_manager.flight_info.surface_altitude > max_q_altitude and not max_q_passed:
                    max_q_passed = True
                    self.add_event_log("Max Q Passed - Maximum dynamic pressure altitude reached")
                await asyncio.sleep(1)
        finally:
            vessel = self.vessel_manager.vessel
            await self.activate_next_stage_async()
            vessel.control.sas = True
            await asyncio.sleep(2)  # 姿勢が安定するまで待機
            vessel.control.sas_mode = SASMode.anti_radial  # アンチラジアル
            self.add_event_log("Launch successful - The rocket has reached the target orbit")

    async def activate_next_stage_async(self: "FlightManager") -> None:
        """次のステージを非同期でアクティブにする関数"""
        await asyncio.get_event_loop().run_in_executor(
            self.executor,
            self.vessel_manager.vessel.control.activate_next_stage,
        )

    async def get_telemetry(self: "FlightManager") -> dict:
        """Get telemetry data for the rocket."""
        return {
            "time": datetime.now(timezone.utc).isoformat(),
            "launch_relative_time": self.launch_relative_time,
            "flight_records": await LogManager.read_log_file_async(self.log_file_path),
            "event_records": await LogManager.read_log_file_with_key_async(self.log_file_path, "event"),
            "rocket_status": await asyncio.get_event_loop().run_in_executor(
                self.executor,
                self.status_manager.get_rocket_status,
            ),
            "vessel_telemetry": await asyncio.get_event_loop().run_in_executor(
                self.executor,
                self.telemetry_manager.get_vessel_telemetry,
            ),
        }

    def flight_record_data(self: "FlightManager") -> dict[str, Any] | None:
        """飛行データを記録する"""
        try:
            finfo = self.vessel_manager.flight_info
            orbit = self.vessel_manager.orbit
            return {
                "time": datetime.now(timezone.utc).isoformat(),
                "launch_relative_time": self.launch_relative_time,
                "heading": finfo.heading,
                "altitude": finfo.surface_altitude,
                "latitude": finfo.latitude,
                "longitude": finfo.longitude,
                "orbital_speed": orbit.speed,
                "apoapsis_altitude": orbit.apoapsis_altitude,
                "periapsis_altitude": orbit.periapsis_altitude,
                "inclination": orbit.inclination,
                "eccentricity": orbit.eccentricity,
            }
        except Exception:
            logger.exception("Error recording flight data")
            return None

    def add_event_log(self: "FlightManager", msg: str) -> None:
        """イベントログを追加する"""
        flight_data = self.flight_record_data()
        if flight_data is None:
            logger.error("Failed to get flight data for event log.")
            return

        new_data = {"event": msg}
        flight_data.update(new_data)
        if flight_data:
            LogManager.save_to_log_sync(flight_data, self.log_file_path)
