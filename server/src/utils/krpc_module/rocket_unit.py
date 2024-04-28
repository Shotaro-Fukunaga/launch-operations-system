from krpc.services.spacecenter import Part, Vessel


class Unit:
    """ロケットのパーツを管理するユニットクラス"""
    def __init__(self: "Unit", vessel: Vessel, unit_name: str, group_name: str, tag: str, part_type: str, event_type: str, event_details: str, status: int = 0):
        """initializer"""
        self.vessel = vessel
        self.tag = tag
        self.status = status
        self.unit_name = unit_name
        self.part_type = part_type
        self.group_name = group_name
        self.event_type = event_type
        self.event_details = event_details
        self.part: Part = self.find_part_by_tag()

    def find_part_by_tag(self) -> Part | None:
        """タグに基づいたパーツを返す。（タグは一意である必要がある）"""
        for part in self.vessel.parts.all:
            if part.tag == self.tag:
                return part
        return None

    def activate_engine(self) -> dict:
        """エンジンが存在し、アクティブであればステータスを更新"""
        if self.part and getattr(self.part, "engine", None) and self.part.engine.active and self.status == 0:
            self.status = 1
            return {"event_type": f"{self.unit_name} Ignition", "event_details": "Engine is now active."}

    def deploy_solar_panels(self) -> dict:
        """ソーラーパネルが存在し、展開されていればステータスを更新"""
        if self.part and getattr(self.part, "solar_panel", None) and self.part.solar_panel.deployed and self.status == 0:
            self.status = 1
            return {"event_type": f"{self.unit_name} Deployed", "event_details": "All solar panels have been deployed."}

    def fairing_jettisoned(self) -> dict:
        """フェアリングが存在し、ジェットされていればステータスを更新"""
        if self.part and getattr(self.part, "fairing", None) and self.part.fairing.jettisoned and self.status == 0:
            self.status = 2
            return {"event_type": f"{self.unit_name} Jettisoned", "event_details": f"{self.unit_name} fairings have been jettisoned."}

    def update(self) -> dict:
        """パーツタイプに応じて適切なアクションを実行"""
        if not self.part:
            if self.status != 2:
                self.status = 2
                return {"event_type": self.event_type, "event_details": self.event_details}
        elif self.part_type == "engine":
            return self.activate_engine()
        elif self.part_type == "solar_panel":
            return self.deploy_solar_panels()
        elif self.part_type == "fairing":
            return self.fairing_jettisoned()

    def get_temperature(self) -> dict:
        """パーツの温度と最大温度を返す"""
        temperature = getattr(self.part, "temperature", None)
        max_temperature = getattr(self.part, "max_temperature", None)
        skin_temperature = getattr(self.part, "skin_temperature", None)
        max_skin_temperature = getattr(self.part, "max_skin_temperature", None)

        if temperature is not None and max_temperature and max_temperature != 0:
            thermal_percentage = temperature / max_temperature * 100
        else:
            thermal_percentage = None

        return {
            "temperature": temperature,
            "max_temperature": max_temperature,
            "skin_temperature": skin_temperature,
            "max_skin_temperature": max_skin_temperature,
            "thermal_percentage": thermal_percentage,
        }

    def get_fuel_status(self) -> list[dict]:
        """パーツタイプが 'tank' の場合、燃料のステータスを返す"""
        if self.part_type != "tank" or not self.part:
            return None

        resource_list = []
        resources = self.part.resources.all

        for resource in resources:
            percentage = (resource.amount / resource.max * 100) if resource.max > 0 else 0
            resource_list.append(
                {
                    "name": resource.name,
                    "amount": resource.amount,
                    "max": resource.max,
                    "percentage": percentage,
                }
            )

        return resource_list
