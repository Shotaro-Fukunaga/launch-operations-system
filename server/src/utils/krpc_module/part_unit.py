from krpc.services.spacecenter import Part, Vessel


class PartUnit:
    """ロケットのパーツを管理するユニットクラス"""

    def __init__(self, vessel: Vessel, config: dict):
        """initializer using a configuration dictionary"""
        self.vessel: Vessel = vessel
        self.unit_name: str = config["unit_name"]
        self.group_name: str = config["group_name"]
        self.tag: str = config["tag"]
        self.part_type: str = config["part_type"]
        self.status: int = config["status"]
        self.part: Part | None = self.find_part()

    def find_part(self) -> Part | None:
        """"""
        for part in self.vessel.parts.all:
            if part.tag == self.tag:
                return part
        return None

    def update(self):
        self.part = self.find_part()
