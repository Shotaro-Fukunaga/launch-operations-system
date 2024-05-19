from krpc.services.spacecenter import Part, Vessel


class PartUnit:
    """ロケットのパーツを管理するユニットクラス"""

    def __init__(self: "PartUnit", vessel: Vessel, config: dict)-> None:
        """Initialize the PartUnit class.

        Status:
            WAIT   : 0 待機中
            GO     : 1 準備完了
            ACTIVE : 2 動作中
            CUTOFF : 3 カットオフ
        """
        self.vessel: Vessel = vessel
        self.unit_name: str = config["unit_name"]
        self.group_name: str = config["group_name"]
        self.tag: str = config["tag"]
        self.part_type: str = config["part_type"]

        self.status: int = config["status"]
        self.part: Part | None = self.find_part()

    def find_part(self: "PartUnit") -> Part | None:
        """タグが一致するパーツを検索して返す"""
        for part in self.vessel.parts.all:
            if part.tag == self.tag:
                return part
        return None

    def update(self: "PartUnit") -> None:
        """ユニットのパーツを更新する"""
        self.part = self.find_part()
