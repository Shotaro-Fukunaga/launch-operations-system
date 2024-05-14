import logging

from krpc.services import Client

from src.utils.krpc_module.part_unit import PartUnit

logger = logging.getLogger(__name__)


class VesselManager:
    """ロケットの部品とKRPCのインスタンスを管理するクラス"""

    def __init__(self: "VesselManager", client: Client, rocket_schema_list: list[dict]) -> None:
        """Initialize"""
        self.client = client
        if client.space_center is None:
            error_message = "client.space_center is None. Cannot access active_vessel."
            raise ValueError(error_message)

        self.vessel = client.space_center.active_vessel
        # MechJeb2のインスタンスだが、KRPCの型定義には存在しないためignore
        self.mech_jeb = client.mech_jeb  # type: ignore
        self.orbit = self.vessel.orbit
        self.reference_frame = self.vessel.orbit.body.reference_frame
        self.flight_info = self.vessel.flight(self.reference_frame)
        self.rocket_schema_list = rocket_schema_list
        self.unit_initiliaze()

    def unit_initiliaze(self: "VesselManager") -> None:
        """各PartUnitを初期化する"""
        self.units: dict[str, PartUnit] = {config["tag"]: PartUnit(vessel=self.vessel, config=config) for config in self.rocket_schema_list}

    def set_all_units_status(self: "VesselManager", status: int) -> None:
        """全てのPartUnitのステータスを更新する

        Args:
            status (int): 新しいステータス値
        """
        for unit in self.units.values():
            unit.status = status

    def get_units_by_part_type(self: "VesselManager", part_type: str) -> list[PartUnit]:
        """指定された部品タイプのPartUnitを取得する

        Args:
            part_type (str): 検索する部品タイプ

        Returns:
            list[PartUnit]: 一致するPartUnitのリスト
        """
        return [unit for unit in self.units.values() if unit.part_type == part_type]

    def get_unit_group_name(self: "VesselManager", group_name: str) -> list[PartUnit]:
        """指定されたグループ名のPartUnitを取得する

        Args:
            group_name (str): 検索するグループ名

        Returns:
            list[PartUnit]: 一致するPartUnitのリスト
        """
        return [unit for unit in self.units.values() if unit.group_name == group_name]

    def get_unit_by_name(self: "VesselManager", unit_name: str) -> PartUnit | None:
        """指定された名前のPartUnitを取得する

        Args:
            unit_name (str): 検索するユニット名

        Returns:
            PartUnit|None: 一致するPartUnit、またはNone
        """
        for unit in self.units.values():
            if unit.unit_name == unit_name:
                unit.update()
                return unit
        return None
