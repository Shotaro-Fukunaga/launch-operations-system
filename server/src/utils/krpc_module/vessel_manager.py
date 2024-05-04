from src.utils.krpc_module.part_unit import PartUnit
from krpc.services import Client


class VesselManager:

    def __init__(self, client: Client, rocket_schema_list):
        self.client = client
        self.vessel = client.space_center.active_vessel
        self.orbit = self.vessel.orbit
        self.reference_frame = self.vessel.orbit.body.reference_frame
        self.flight_info = self.vessel.flight(self.reference_frame)
        self.rocket_schema_list = rocket_schema_list
        self.unit_initiliaze()

    def unit_initiliaze(self) -> None:
        self.units: dict[str, PartUnit] = {config["tag"]: PartUnit(vessel=self.vessel, config=config) for config in self.rocket_schema_list}

    def set_all_units_status(self, status: int) -> None:
        # unitsディクショナリ内の全PartUnitのstatusを更新
        for unit in self.units.values():
            unit.status = status


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
