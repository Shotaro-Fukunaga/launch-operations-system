import math
import logging
from datetime import datetime, timezone
from src.utils.krpc_module.rocket_core import RocketCore
import json

logger = logging.getLogger(__name__)


# TODO あとでリファクタリング
class EventManager:
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
        self.rocket_core = rocket_core
        self.orbit = rocket_core.orbit
        self.launch_date = launch_datetime
        self.target_periapsis = target_periapsis
        self.target_apoapsis = target_apoapsis
        self.target_orbit_inc = target_orbit_inc
        self.flight_id = flight_id
        self.max_q_altitude = max_q_altitude
        self.target_orbit_speed = target_orbit_speed
        self.event_records = []

    def record_event_data(self, event_type: str, event_details: str, is_significant_event=False):
        event_data = {
            "time": datetime.now(timezone.utc),
            "event_type": event_type,
            "event_details": event_details,
            "is_significant_event": is_significant_event,
        }
        logger.info(f"{event_type} at {event_data['time']}: {event_details}")
        self.event_records.append(event_data)

    def event_update(self):
        event_data = []
        event_data.extend(
            [
                self._check_max_q_passed(),
                self._check_orbital_speed(),
                self._check_apoapsis(),
                self._check_periapsis(),
                self._check_arrived_target_orbit(),
            ]
        )

        for unit in self.rocket_core.units.values():
            event = unit.update()
            if event:
                event_data.append({"event_type": event["event_type"], "event_details": event["event_details"], "is_significant": True})

        if event_data:
            for event in event_data:
                self.record_event_data(event["event_type"], event["event_details"], event["is_significant"])

    def get_events(self) -> list[dict]:
        return self.event_records

    def save_event_records(self) -> None:
        file_path = f"src/event_records/{self.flight_id}.json"
        json_data = {"flight_id": self.flight_id, "flight_records": self.event_records}
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
