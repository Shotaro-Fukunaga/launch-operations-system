import logging

from src.config import STANDBY, ACTIVE, DETACHED
from src.utils.krpc_module.vessel_manager import VesselManager
from src.utils.krpc_module.part_unit import PartUnit
import json

from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class EventManager:

    def __init__(
        self,
        vessel_manager: VesselManager,
    ):
        self.vessel_manager = vessel_manager
        self.orbit = vessel_manager.orbit
        self.flight_info = vessel_manager.flight_info
        self.units: list[PartUnit] = vessel_manager.units.values()
        # VesselManagerのflight_recordsに参照でリンクさせる
        self.records: list = self.vessel_manager.flight_records
        self.max_q_passed = False
        self.orbital_speed_exceeded = False
        self.apoapsis_exceeded = False
        self.periapsis_exceeded = False
        self.set_target_orbit()

    def set_target_orbit(
        self,
        target_apoapsis=0,
        target_periapsis=0,
        target_orbit_speed=0,
        target_orbit_inc=0,
        max_q_altitude=0,
    ) -> None:
        self.target_apoapsis = target_apoapsis
        self.target_periapsis = target_periapsis
        self.target_orbit_speed = target_orbit_speed
        self.target_orbit_inc = target_orbit_inc
        self.max_q_altitude = max_q_altitude

    def clear_records(self) -> None:
        self.records = []

    def get_records(self) -> list[dict]:
        return self.records

    def save_records(self) -> None:
        """航空記録をJSONファイルに保存する。"""
        try:
            file_path = "src/flight_records/111.json"
            json_data = {"flight_id": 111, "records": self.records}
            json_string = json.dumps(json_data, indent=4, default=str)
            with open(file_path, "w") as f:
                f.write(json_string)
        except IOError as e:
            logger.error(f"Failed to save records: {e}")

    def record_data(
        self,
        event_type: str = "",
        event_details: str = "",
        event_level: int = 0,
    ) -> None:
        current_time = datetime.now(timezone.utc).replace(microsecond=0)
        event_data = {
            "time": current_time,
            "event_type": event_type,
            "event_details": event_details,
            # 0が通常のレコード、1がログレベル、2が重要なイベント
            "event_level": event_level,
            "heading": self.flight_info.heading,
            "altitude": self.flight_info.surface_altitude,
            "latitude": self.flight_info.latitude,
            "longitude": self.flight_info.longitude,
            "orbital_speed": self.orbit.speed,
            "apoapsis_altitude": self.orbit.apoapsis_altitude,
            "periapsis_altitude": self.orbit.periapsis_altitude,
            "inclination": self.orbit.inclination,
            "eccentricity": self.orbit.eccentricity,
        }
        if event_level != 0:
            logger.info(f"{event_type} at {event_data['time']}: {event_details}")
        self.records.append(event_data)

    def update(self) -> None:
        for unit in self.units:
            unit.update()
            if unit.part_type == "engine":
                self._check_engine(unit)
            elif unit.part_type == "solar_panel":
                self._check_solar_panels(unit)
            elif unit.part_type == "fairing":
                self._check_fairing(unit)
            else:
                self._check_unit(unit)
        self._check_max_q()
        self._check_orbital_speed()
        self._check_apoapsis()
        self._check_periapsis()
        self.record_empty_data()

    def record_empty_data(self):
        """空のデータを記録する。"""
        self.record_data("", "", 0)

    def _check_unit(self, unit: PartUnit) -> None:
        if not unit.part and unit.status != DETACHED:
            unit.status = DETACHED
            event_type = f"{unit.unit_name.capitalize()} Cutoff."
            event_details = f"{unit.unit_name.replace('_', ' ')} cutoff."
            self.record_data(event_type, event_details, 2)

    def _check_engine(self, unit: PartUnit) -> None:
        """エンジンの点火が成功したかどうかを確認し、結果を記録する。"""
        part = unit.part
        if part and hasattr(part, "engine") and part.engine.active and unit.status == STANDBY:
            unit.status = ACTIVE
            event_type = f"{unit.unit_name.capitalize()} Ignition"
            event_details = f"{unit.unit_name.replace('_', ' ')} has been ignited."
            self.record_data(event_type, event_details, 2)
        elif not part and unit.status != DETACHED:
            unit.status = DETACHED
            event_type = "MECO" if "main_engine" in unit.unit_name else "SECO"
            event_details = f"{unit.unit_name.replace('_', ' ')} cutoff."
            self.record_data(event_type, event_details, 2)

    def _check_solar_panels(self, unit: PartUnit) -> None:
        """Check if the solar panel is deployed and update its status."""
        part = unit.part
        if part and hasattr(part, "solar_panel") and part.solar_panel:
            if part.solar_panel.deployed and unit.status == STANDBY:
                unit.status = ACTIVE
                event_type = f"{unit.unit_name.capitalize()} Deployed"
                event_details = f"{unit.unit_name.replace('_', ' ')} has been deployed."
                self.record_data(event_type, event_details, 2)

    def _check_fairing(self, unit: PartUnit) -> None:
        """Check if the fairing has been jettisoned and update its status."""
        if not unit.part and unit.status != DETACHED:
            unit.status = DETACHED
            event_type = f"{unit.unit_name.capitalize()} Jettisoned"
            event_details = f"{unit.unit_name.replace('_', ' ')} has been jettisoned."
            self.record_data(event_type, event_details, 2)

    def _check_max_q(self) -> None:
        """Check if the vessel has passed the maximum dynamic pressure."""
        current_altitude = self.flight_info.surface_altitude
        if self.max_q_altitude == current_altitude and not self.max_q_passed:
            self.max_q_passed = True
            self.record_data("Max Q Passed", "Max Q altitude has been passed.", 2)

    def _check_orbital_speed(self) -> None:
        """Check if the vessel's orbital speed has exceeded the target speed."""
        current_speed = self.orbit.speed
        if current_speed > self.target_orbit_speed and not self.orbital_speed_exceeded:
            self.orbital_speed_exceeded = True
            self.record_data("Orbital Speed Exceeded", f"Orbital speed is greater than {self.target_orbit_speed} m/s.", 2)

    def _check_apoapsis(self) -> None:
        """Check if the vessel's apoapsis has exceeded the target altitude."""
        current_apoapsis = self.orbit.apoapsis_altitude
        if current_apoapsis > self.target_apoapsis and not self.apoapsis_exceeded:
            self.apoapsis_exceeded = True
            self.record_data("Apoapsis Exceeded", f"Apoapsis altitude is greater than {self.target_apoapsis} m.", 2)

    def _check_periapsis(self) -> None:
        """Check if the vessel's periapsis has exceeded the target altitude."""
        current_periapsis = self.orbit.periapsis_altitude
        if current_periapsis > self.target_periapsis and not self.periapsis_exceeded:
            self.periapsis_exceeded = True
            self.record_data("Periapsis Exceeded", f"Periapsis altitude is greater than {self.target_periapsis} m.", 2)