from src.utils.krpc_module.part_unit import PartUnit
from src.utils.krpc_module.telemetry_manager import TelemetryManager
from krpc.services import Client


class VesselManager:

    def __init__(self, client: Client, rocket_schema_list):
        self.client = client
        self.vessel = client.space_center.active_vessel
        self.orbit = self.vessel.orbit
        self.reference_frame = self.vessel.orbit.body.reference_frame
        self.flight_info = self.vessel.flight(self.reference_frame)
        self.telemetry_manager = TelemetryManager(self)
        self.rocket_schema_list = rocket_schema_list
        self.flight_records = []
        self.unit_initiliaze()

    def unit_initiliaze(self) -> None:
        self.units: dict[str, PartUnit] = {config["tag"]: PartUnit(vessel=self.vessel, config=config) for config in self.rocket_schema_list}

    def get_vessel_telemetry(self):
        """TelemetryManager を通じてテレメトリ情報を取得する"""
        return self.telemetry_manager.get_vessel_telemetry()

    def get_rocket_status(self):
        """TelemetryManager を通じてロケットのステータスを取得する"""
        return self.telemetry_manager.get_rocket_status()

    def get_flight_records(self) -> list[dict]:
        return self.flight_records

    def get_units_by_part_type(self, part_type) -> list[PartUnit]:
        unit_list = []
        for unit in self.units.values():
            if unit.part_type == part_type:
                unit_list.append(unit)
        return unit_list

    def get_unit_group_name(self, group_name) -> list:
        unit_list = []
        for unit in self.units.values():
            if unit.group_name == group_name:
                unit_list.append(unit)
        return unit_list

    def get_unit_by_name(self, unit_name) -> PartUnit:
        for unit in self.units.values():
            if unit.unit_name == unit_name:
                return unit
        return None

    def get_total_mass_by_group(self, group_name) -> float:
        total_mass = 0
        for unit in self.units.values():
            if unit.group_name == group_name:
                total_mass += getattr(unit.part, "mass", 0)
        return total_mass
