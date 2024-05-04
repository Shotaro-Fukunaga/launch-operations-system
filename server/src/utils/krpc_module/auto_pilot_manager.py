import time
import logging
import threading
from src.settings.config import EVENT_NORMAL, EVENT_IMPORTANT
from datetime import datetime, timezone, timedelta
from src.utils.krpc_module.event_manager import FlightRecorder
from src.utils.krpc_module.krpc_client import KrpcClient
from src.utils.krpc_module.vessel_manager import VesselManager
from src.utils.krpc_module.telemetry_manager import TelemetryManager
from src.settings.config import rocket_schema_list, GO

logger = logging.getLogger(__name__)


# TODO あとでスレッド管理する
class FlightManager:
    def __init__(self):
        self.krpc_client = KrpcClient("LaunchOperationsAPI")
        self.vessel_manager = VesselManager(self.krpc_client.client, rocket_schema_list)
        self.telemetry_manager = TelemetryManager(self.vessel_manager)
        self.event_manager = FlightRecorder(self.vessel_manager,self)
        self.launch_relative_time = "T-00:00:00"
        self.max_q_passed = False
        self.max_q_altitude = 11200

    def countdown_and_countup(self, launch_date: datetime):
        # launch_dateまでのカウントダウンを開始
        while True:
            now = datetime.now(timezone.utc)
            time_diff = launch_date - now
            seconds_remaining = time_diff.total_seconds()
            self.event_manager.update()
            if seconds_remaining > 0:
                self.launch_relative_time = f"T-{timedelta(seconds=int(seconds_remaining))}"
            else:
                self.launch_relative_time = f"T+{timedelta(seconds=int(abs(seconds_remaining)))}"
                break
            time.sleep(1)  # 1秒ごとに更新

        # launch_dateを超えた後のカウントアップを開始
        while True:
            now = datetime.now(timezone.utc)
            time_diff = now - launch_date
            seconds_since_launch = time_diff.total_seconds()
            self.launch_relative_time = f"T+{timedelta(seconds=int(seconds_since_launch))}"
            self.event_manager.update()
            time.sleep(1)

    def _wait_for_launch(self, launch_date: datetime):
        while True:
            time_diff = launch_date - datetime.now(timezone.utc)
            if time_diff.total_seconds() <= 0:
                break
            self.event_manager.event_record_data(f"Waiting for launch: {time_diff.total_seconds()} seconds remaining", EVENT_NORMAL)
            time.sleep(1)

    def sequence_start(
        self,
        launch_date: datetime,
        target_periapsis: int,
        target_apoapsis: int,
        target_orbit_inc: float,
        target_orbit_speed: int,
    ):
        self.target_periapsis = target_periapsis
        self.target_apoapsis = target_apoapsis
        self.target_orbit_inc = target_orbit_inc
        self.target_orbit_speed = target_orbit_speed

        launch_relative_time_thread = threading.Thread(
            target=self.countdown_and_countup,
            args=(launch_date,),  # カンマを追加してタプルとして渡す
        )
        launch_relative_time_thread.start()

        self.event_manager.event_record_data("Launch sequence started.", EVENT_IMPORTANT)

        # ユニットを初期化
        self.vessel_manager.set_all_units_status(GO)

        # 打ち上げ時間まで待機
        self._wait_for_launch(launch_date)

        # スレッドを使用してオートパイロットを非同期に実行
        autopilot_thread = threading.Thread(
            target=self.execute_autopilot,
            args=(target_periapsis, target_orbit_inc, target_apoapsis),
        )
        autopilot_thread.start()


    def execute_autopilot(
        self,
        target_orbit_altitude: int,
        target_inclination: float,
        target_apoapsis: int,
    ) -> None:
        vessel = self.vessel_manager.vessel
        mechjeb = self.krpc_client.client.mech_jeb

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
        self.event_manager.event_record_data("Rocket Lift off", EVENT_IMPORTANT)

        max_q_passed = False
        try:
            while ascent_autopilot.enabled:

                if self.vessel_manager.flight_info.surface_altitude > self.max_q_altitude and not max_q_passed:
                    max_q_passed = True
                    self.event_manager.event_record_data("Max Q Passed", EVENT_IMPORTANT)
                time.sleep(1)
        finally:
            self.post_ascent_tasks()

    def post_ascent_tasks(self):
        """ Perform post-ascent tasks. """
        vessel = self.vessel_manager.vessel
        vessel.control.activate_next_stage()
        vessel.control.sas = True
        time.sleep(3)  # Wait for SAS to stabilize
        vessel.control.set_sas_mode('anti_radial')

        current_periapsis = vessel.orbit.periapsis_altitude
        periapsis_diff = current_periapsis - self.target_periapsis
        current_apoapsis = vessel.orbit.apoapsis_altitude
        apoapsis_diff = current_apoapsis - self.target_apoapsis
        current_speed = vessel.orbit.speed
        speed_diff = current_speed - self.target_orbit_speed

        self.event_manager.event_record_data(f"Periapsis Difference: {periapsis_diff} m", EVENT_IMPORTANT)
        self.event_manager.event_record_data(f"Apoapsis Difference: {apoapsis_diff} m", EVENT_IMPORTANT)
        self.event_manager.event_record_data(f"Speed Difference: {speed_diff} m/s", EVENT_IMPORTANT)
        self.event_manager.event_record_data("Launch sequence completed.", EVENT_IMPORTANT)
        self.event_manager.save_records()

    def get_telemetry(self) -> list[dict]:
        return {
            "time": datetime.now(timezone.utc).isoformat(),
            "launch_relative_time": self.launch_relative_time,
            "flight_records": self.event_manager.flight_records,
            "event_records": self.event_manager.event_records,
            "rocket_status": self.telemetry_manager.get_rocket_status(),
            "vessel_telemetry": self.telemetry_manager.get_vessel_telemetry(),
        }