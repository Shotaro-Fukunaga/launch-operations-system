import logging
from datetime import datetime, timezone
import json
import time
from src.utils.krpc_module.rocket_core import RocketCore


logger = logging.getLogger(__name__)


class FlightManager:
    """ロケットの飛行管理を行うクラス"""

    def __init__(
        self,
        rocket_core: RocketCore,
        launch_datetime,
        target_periapsis,
        target_apoapsis,
        target_orbit_inc,
        flight_id,
        max_q_altitude,
        target_orbit_speed,
    ):
        """initialize FlightManager"""
        self.rocket_core = rocket_core
        self.mission_complete = False
        self.launch_date = launch_datetime
        self.target_periapsis = target_periapsis
        self.target_apoapsis = target_apoapsis
        self.target_orbit_inc = target_orbit_inc
        self.flight_id = flight_id
        self.max_q_altitude = max_q_altitude
        self.target_orbit_speed = target_orbit_speed
        self.flight_records = []

    def launch_sequence(self):
        """打ち上げシーケンスを実行
        指定された打ち上げ時刻まで待機後、自動飛行パイロットでの昇降と軌道投入を開始
        """
        self.wait_for_launch(self.launch_date)
        self.execute_autopilot(
            self.target_periapsis,
            self.target_orbit_inc,
            self.target_apoapsis,
        )

    def wait_for_launch(self, launch_date: datetime):
        """指定された打ち上げ時刻まで待機する
        Args:
            launch_date (datetime): 打ち上げ予定日時
        """
        while True:
            time_diff = launch_date - datetime.now(timezone.utc)
            if time_diff.total_seconds() <= 0:
                break
            logger.info(f"Waiting for launch: {time_diff.total_seconds()} seconds remaining")
            time.sleep(1)

    def get_flight_records(self) -> list[dict]:
        return self.flight_records

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
        vessel = self.rocket_core.vessel
        mechjeb = self.rocket_core.conn.mech_jeb

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

        # Wait for launch to complete
        while ascent_autopilot.enabled:
            self.record_flight_data()
            time.sleep(1)

        vessel.control.activate_next_stage()
        vessel.auto_pilot.target_direction = (0, 0, 1)

        self.mission_complete = True
        self.save_flight_records(save_to_file=True)

    def record_flight_data(self) -> None:
        """現在のロケットの状態を取得し、flight_recordsに追加"""
        self.flight_records.append(
            {
                "time": datetime.now(timezone.utc),
                "heading": self.rocket_core.flight_info.heading,
                "altitude": self.rocket_core.flight_info.surface_altitude,
                "latitude": self.rocket_core.flight_info.latitude,
                "longitude": self.rocket_core.flight_info.longitude,
                "orbital_speed": self.rocket_core.orbit.speed,
                "apoapsis_altitude": self.rocket_core.orbit.apoapsis_altitude,
                "periapsis_altitude": self.rocket_core.orbit.periapsis_altitude,
                "inclination": self.rocket_core.orbit.inclination,
                "eccentricity": self.rocket_core.orbit.eccentricity,
            }
        )

    def get_flight_records(self) -> list[dict]:
        """飛行データを返す

        Returns:
            list[dict]: 飛行データのリスト
        """
        return self.flight_records

    def save_flight_records(self) -> None:
        """飛行記録をJSON形式でファイルに保存"""
        file_path = f"src/flight_records/{self.flight_id}.json"
        json_data = {"flight_id": self.flight_id, "flight_records": self.flight_records}
        json_string = json.dumps(json_data, indent=4, default=str)

        with open(file_path, "w") as f:
            f.write(json_string)
