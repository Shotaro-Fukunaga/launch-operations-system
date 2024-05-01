import math
import logging
from datetime import datetime, timezone
from src.utils.krpc_module.rocket_core import RocketCore
import json
import time
import threading
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)


# TODO あとでリファクタリング
# レコードを管理するクラスをオートパイロットクラスに継承して、レコードを保持する
# 
class RecordManager:
    def __init__(self, rocket_core: RocketCore):
        self.rocket_core = rocket_core
        self.orbit = rocket_core.orbit
        self.launch_date = datetime.now(timezone.utc) + timedelta(seconds=10)
        self.target_periapsis = 200000
        self.target_apoapsis = 200000
        self.target_orbit_inc = 30.39
        self.flight_id = 121
        self.max_q_altitude = 11200
        self.target_orbit_speed = 7788
        self.records = []

    def launch_sequence(self):
        self.wait_for_launch(self.launch_date)
        # スレッドを使用してオートパイロットを非同期に実行
        autopilot_thread = threading.Thread(
            target=self.execute_autopilot,
            args=(
                self.target_periapsis,
                self.target_orbit_inc,
                self.target_apoapsis,
            ),
        )
        autopilot_thread.start()
        return "Launch sequence started."

    def wait_for_launch(self, launch_date: datetime):
        while True:
            time_diff = launch_date - datetime.now(timezone.utc)
            if time_diff.total_seconds() <= 0:
                break
            logger.info(f"Waiting for launch: {time_diff.total_seconds()} seconds remaining")
            time.sleep(1)

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
            self.record_update()
            time.sleep(1)

        vessel.control.activate_next_stage()
        vessel.auto_pilot.target_direction = (0, 0, 1)

        self.mission_complete = True
        self.save_records()
        self.records = []

    def record_data(self, event_type: str = "", event_details: str = "", event_level: int = 0):
        event_data = {
            "time": datetime.now(timezone.utc),
            "event_type": event_type,
            "event_details": event_details,
            # 0が通常のレコード、1がログレベル、2が重要なイベント
            "event_level": event_level,
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
        logger.info(f"{event_type} at {event_data['time']}: {event_details}")
        self.records.append(event_data)

    def record_update(self):
        self.record_data()
        event_data = []
        # event_data.extend(
        #     [
        #         self._check_max_q_passed(),
        #         self._check_orbital_speed(),
        #         self._check_apoapsis(),
        #         self._check_periapsis(),
        #         self._check_arrived_target_orbit(),
        #     ]
        # )

        # for unit in self.rocket_core.units.values():
        #     event = unit.update()
        #     if event:
        #         event_data.append(
        #             {
        #                 "event_type": event["event_type"],
        #                 "event_details": event["event_details"],
        #                 "event_level": 2,
        #             }
        #         )

        # if event_data:
        #     for event in event_data:
        #         self.record_data(
        #             event["event_type"],
        #             event["event_details"],
        #             event["event_level"],
        #         )
        # else:
        #     self.record_data()

    def clear_records(self):
        self.records = []

    def get_records(self) -> list[dict]:
        return self.records

    def save_records(self) -> None:
        file_path = f"src/flight_records/{self.flight_id}.json"
        json_data = {"flight_id": self.flight_id, "records": self.records}
        json_string = json.dumps(json_data, indent=4, default=str)

        with open(file_path, "w") as f:
            f.write(json_string)

    def _check_max_q_passed(self):
        current_altitude = self.rocket_core.flight_info.surface_altitude
        if self.max_q_altitude == current_altitude["altitude_als"]:
            return {
                "event_type": "Max Q Passed",
                "event_details": "Max Q altitude has been passed.",
                "is_significant": True,
            }

    def _check_orbital_speed(self):
        target_orbit_speed = self.target_orbit_speed
        current_orbit_speed = self.rocket_core.orbit.orbital_speed
        if current_orbit_speed > target_orbit_speed:
            return {
                "event_type": "Orbital Speed Exceeded",
                "event_details": f"Orbital speed is greater than {target_orbit_speed} m/s.",
                "is_significant": True,
            }

    def _check_apoapsis(self):
        target_apoapsis = self.target_apoapsis
        current_apoapsis = self.orbit.apoapsis_altitude
        if current_apoapsis > target_apoapsis:
            return {
                "event_type": "Apoapsis Exceeded",
                "event_details": f"Apoapsis altitude is greater than {target_apoapsis} m.",
                "is_significant": True,
            }

    def _check_periapsis(self):
        target_periapsis = self.target_periapsis
        current_periapsis = self.orbit.periapsis_altitude
        if current_periapsis > target_periapsis:
            return {
                "event_type": "Periapsis Exceeded",
                "event_details": f"Periapsis altitude is greater than {target_periapsis} m.",
                "is_significant": True,
            }

    def _check_arrived_target_orbit(self):
        current_periapsis = self.orbit.periapsis_altitude
        current_apoapsis = self.orbit.apoapsis_altitude
        current_inclination_degrees = math.degrees(self.orbit.inclination)

        # 許容誤差範囲を定義
        periapsis_tolerance = 1500  # メートル
        apoapsis_tolerance = 1500  # メートル
        inclination_tolerance = 1  # 度

        if (
            abs(current_periapsis - self.target_periapsis) <= periapsis_tolerance
            and abs(current_apoapsis - self.target_apoapsis) <= apoapsis_tolerance
            and abs(current_inclination_degrees - self.target_orbit_inc) <= inclination_tolerance
        ):
            return {"event_type": "Target Orbit Achieved", "event_details": "The vessel has reached the target orbit.", "is_significant": True}
