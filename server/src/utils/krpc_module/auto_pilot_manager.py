import time
import logging
import threading
from datetime import datetime, timezone
from src.utils.krpc_module.event_manager import EventManager
from src.utils.krpc_module.vessel_manager import VesselManager

logger = logging.getLogger(__name__)


class AutoPilotManager:
    def __init__(self, vessel_manager: VesselManager):
        self.vessel_manager = vessel_manager
        self.vessel = vessel_manager.vessel
        self.client = vessel_manager.client
        self.event_manager = EventManager(vessel_manager)

    def _wait_for_launch(self, launch_date: datetime):
        while True:
            time_diff = launch_date - datetime.now(timezone.utc)
            if time_diff.total_seconds() <= 0:
                break
            logger.info(f"Waiting for launch: {time_diff.total_seconds()} seconds remaining")
            time.sleep(1)

    def launch_sequence(
        self,
        launch_date: datetime,
        target_periapsis: int = 200000,
        target_apoapsis: int = 200000,
        target_orbit_inc: float = 39.39,
        target_orbit_speed: int = 7788,
        max_q_altitude: int = 11200,
    ):
        # ユニットを初期化
        self.vessel_manager.unit_initiliaze()

        self.event_manager.set_target_orbit(
            target_periapsis=target_periapsis,
            target_apoapsis=target_apoapsis,
            target_orbit_speed=target_orbit_speed,
            target_orbit_inc=target_orbit_inc,
            max_q_altitude=max_q_altitude,
        )

        # 打ち上げ時間まで待機
        self._wait_for_launch(launch_date)

        # スレッドを使用してオートパイロットを非同期に実行
        autopilot_thread = threading.Thread(
            target=self.execute_autopilot,
            args=(target_periapsis, target_orbit_inc, target_apoapsis),
        )
        autopilot_thread.start()

        return "Launch sequence started."

    def post_ascent_tasks(self):
        # アクティベート次のステージ
        self.vessel.control.activate_next_stage()

        # SASを有効にし、ラジアルイン方向に設定
        self.vessel.control.sas = True  # SASを有効にする
        time.sleep(1)  # SASが有効化されるのを少し待つ
        self.vessel.control.sas_mode = self.vessel.control.sas_mode.anti_radial

        # 打ち上げ完了とその記録
        self.event_manager.record_data("Launch", "Launch sequence completed.", 2)
        self.event_manager.save_records()
        self.event_manager.clear_records()

    def execute_autopilot(
        self,
        target_orbit_altitude: int,
        target_inclination: float,
        target_apoapsis: int,
    ) -> None:
        """Mechjebのオートパイロットを実行

        References:
            https://genhis.github.io/KRPC.MechJeb/python/ascent-autopilot.html#MechJeb.AscentPVG

        Args:
            target_orbit_altitude (int): 目標軌道高度
            target_inclination (float): 目標軌道傾斜角
            target_apoapsis (int): 目標アポアプシス高度
        """
        vessel = self.vessel
        mechjeb = self.client.mech_jeb

        # Get the ascent autopilot module
        ascent_autopilot = mechjeb.ascent_autopilot
        ascent_path_guidance = ascent_autopilot.ascent_path_pvg
        ascent_autopilot.ascent_path_index = 2

        # Configure autopilot settings
        ascent_autopilot.desired_orbit_altitude = target_orbit_altitude
        ascent_autopilot.desired_inclination = target_inclination
        ascent_path_guidance.desired_apoapsis = target_apoapsis
        ascent_autopilot.force_roll = True
        ascent_autopilot.turn_roll = 90
        ascent_autopilot.autodeploy_solar_panels = True
        ascent_autopilot.auto_deploy_antennas = True
        ascent_autopilot.autostage = True
        ascent_autopilot.enabled = True

        vessel.control.activate_next_stage()

        try:
            while ascent_autopilot.enabled:
                self.event_manager.update()
                time.sleep(1)
        finally:
            self.post_ascent_tasks()
