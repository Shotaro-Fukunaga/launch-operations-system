import logging

from src.settings.config import STANDBY, ACTIVE, DEPLOYED, CUTOFF, EVENT_NORMAL, EVENT_IMPORTANT, EVENT_ERROR
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
        # VesselManagerのevent_recordsに参照でリンクさせる
        self.records: list = self.vessel_manager.event_records
        self.max_q_passed = False
        self.max_q_altitude = 11200

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
        event_details: str = "",
        event_level: int = EVENT_NORMAL,
    ) -> None:
        """イベントデータを記録する。"""
        event_data = {
            "time": datetime.now(timezone.utc).isoformat(),
            "event_details": event_details,
            "event_level": event_level,
        }
        logger.info(f"{event_data['time']}: {event_details}")
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

    def _check_unit(self, unit: PartUnit) -> None:
        if not unit.part and unit.status != CUTOFF:
            unit.status = CUTOFF
            event_details = f"{unit.unit_name.capitalize().replace('_', ' ')} Cutoff."
            self.record_data(event_details, EVENT_NORMAL)

    def _check_engine(self, unit: PartUnit) -> None:
        """エンジンの点火が成功したかどうかを確認し、結果を記録する。"""
        part = unit.part
        if part and hasattr(part, "engine") and part.engine.active and unit.status == STANDBY:
            unit.status = ACTIVE
            event_details = f"{unit.unit_name.capitalize().replace('_', ' ')} Ignition"
            self.record_data(event_details, EVENT_NORMAL)
        elif not part and unit.status != CUTOFF:
            unit.status = CUTOFF
            event_details = "MECO main engine cutoff. " if "main_engine" in unit.unit_name else "SECO second engine cutoff."
            self.record_data(event_details, EVENT_IMPORTANT)

    def _check_solar_panels(self, unit: PartUnit) -> None:
        """Check if the solar panel is deployed and update its status."""
        part = unit.part
        if part and hasattr(part, "solar_panel") and part.solar_panel:
            if part.solar_panel.deployed and unit.status == STANDBY:
                unit.status = DEPLOYED
                event_details = f"{unit.unit_name.capitalize().replace('_', ' ')} Deployed"
                self.record_data(event_details, EVENT_NORMAL)

    def _check_fairing(self, unit: PartUnit) -> None:
        """Check if the fairing has been jettisoned and update its status."""
        if not unit.part and unit.status != CUTOFF:
            unit.status = CUTOFF
            event_details = f"{unit.unit_name.capitalize().replace('_', ' ')} Jettisoned"
            self.record_data(event_details, EVENT_IMPORTANT)

    def _check_max_q(self) -> None:
        """Check if the vessel has passed the maximum dynamic pressure."""
        current_altitude = self.flight_info.surface_altitude
        if current_altitude > self.max_q_altitude and not self.max_q_passed:
            self.max_q_passed = True
            self.record_data("Max Q Passed", EVENT_IMPORTANT)
