import logging
from typing import TYPE_CHECKING
from src.settings.config import GO, ACTIVE, CUTOFF, EVENT_NORMAL, EVENT_IMPORTANT
from src.utils.krpc_module.vessel_manager import VesselManager
from src.utils.krpc_module.part_unit import PartUnit
import json

from datetime import datetime, timezone


if TYPE_CHECKING:
    from src.utils.krpc_module.auto_pilot_manager import FlightManager

logger = logging.getLogger(__name__)


class FlightRecorder:

    def __init__(self, vessel_manager: VesselManager, flight_manager: "FlightManager"):
        self.vessel_manager = vessel_manager
        self.flight_manager = flight_manager
        self.units: list[PartUnit] = vessel_manager.units.values()
        self.event_records = []
        self.flight_records = []

    def save_records(self) -> None:
        """イベント記録と航空記録を別々のJSONファイルに保存する。"""
        self.save_event_records()
        self.save_flight_records()

    def save_event_records(self) -> None:
        """イベント記録をJSONファイルに保存する。"""
        try:
            file_path = "src/flight_records/event_records.json"
            json_data = {"event_records": self.event_records}
            json_string = json.dumps(json_data, indent=4, default=str)
            with open(file_path, "w") as f:
                f.write(json_string)
            logger.info("Event records saved successfully.")
        except IOError as e:
            logger.error(f"Failed to save event records: {e}")

    def save_flight_records(self) -> None:
        """航空記録をJSONファイルに保存する。"""
        try:
            file_path = "src/flight_records/flight_records.json"
            json_data = {"flight_records": self.flight_records}
            json_string = json.dumps(json_data, indent=4, default=str)
            with open(file_path, "w") as f:
                f.write(json_string)
            logger.info("Flight records saved successfully.")
        except IOError as e:
            logger.error(f"Failed to save flight records: {e}")

    def event_record_data(
        self,
        event_details: str = "",
        event_level: int = EVENT_NORMAL,
    ) -> None:
        """イベントデータを記録する。"""
        event_data = {
            "time": datetime.now(timezone.utc).isoformat(),
            "launch_relative_time": self.flight_manager.launch_relative_time,
            "event_details": event_details,
            "event_level": event_level,
        }
        logger.info(f"{event_data['time']}: {event_details}")
        self.event_records.append(event_data)

    def flight_record_data(self) -> None:
        """飛行データを記録する"""
        flight_info = self.vessel_manager.flight_info
        orbit = self.vessel_manager.orbit
        data = {
            "time": datetime.now(timezone.utc).isoformat(),
            "launch_relative_time": self.flight_manager.launch_relative_time,
            "heading": flight_info.heading,
            "altitude": flight_info.surface_altitude,
            "latitude": flight_info.latitude,
            "longitude": flight_info.longitude,
            "orbital_speed": orbit.speed,
            "apoapsis_altitude": orbit.apoapsis_altitude,
            "periapsis_altitude": orbit.periapsis_altitude,
            "inclination": orbit.inclination,
            "eccentricity": orbit.eccentricity,
        }
        self.flight_records.append(data)

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

    def _check_unit(self, unit: PartUnit) -> None:
        if unit.part and unit.status == GO:
            unit.status = ACTIVE
            event_details = f"{unit.unit_name.capitalize().replace('_', ' ')} ACTIVE"
            self.event_record_data(event_details, EVENT_NORMAL)

        if not unit.part and unit.status != CUTOFF:
            unit.status = CUTOFF
            event_details = f"{unit.unit_name.capitalize().replace('_', ' ')} Cutoff."
            self.event_record_data(event_details, EVENT_NORMAL)

    def _check_engine(self, unit: PartUnit) -> None:
        """エンジンの点火が成功したかどうかを確認し、結果を記録する。"""
        part = unit.part
        if part and hasattr(part, "engine") and part.engine.active and unit.status == GO:
            unit.status = ACTIVE
            event_details = f"{unit.unit_name.capitalize().replace('_', ' ')} Ignition"
            self.event_record_data(event_details, EVENT_NORMAL)
        elif not part and unit.status != CUTOFF:
            unit.status = CUTOFF
            event_details = "MECO main engine cutoff. " if "main_engine" in unit.unit_name else "SECO second engine cutoff."
            self.event_record_data(event_details, EVENT_IMPORTANT)

    def _check_solar_panels(self, unit: PartUnit) -> None:
        """Check if the solar panel is ACTIVE and update its status."""
        part = unit.part
        if part and hasattr(part, "solar_panel") and part.solar_panel:
            if part.solar_panel.deployed and unit.status == GO:
                unit.status = ACTIVE
                event_details = f"{unit.unit_name.capitalize().replace('_', ' ')} ACTIVE"
                self.event_record_data(event_details, EVENT_NORMAL)

    def _check_fairing(self, unit: PartUnit) -> None:
        """Check if the fairing has been jettisoned and update its status."""
        if not unit.part and unit.status != CUTOFF:
            unit.status = CUTOFF
            event_details = f"{unit.unit_name.capitalize().replace('_', ' ')} Jettisoned"
            self.event_record_data(event_details, EVENT_IMPORTANT)
