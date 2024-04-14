class RocketStage:
    def __init__(self, parts):
        """initializer"""
        # ref:  https://krpc.github.io/krpc/python/api/space-center/parts.html
        self.parts = parts

    @property
    def mass(self):
        """ステージの全パーツの質量の合計を返す"""
        return sum(part.mass for part in self.parts)

    @property
    def dry_mass(self):
        """ステージの全パーツの乾燥質量の合計を返す"""
        return sum(part.dry_mass for part in self.parts)

    def get_thermal_data(self):
        """ステージに含まれる各パーツの熱関連データを返す

        Returns:
        - tag: パーツに割り当てられたタグ
        - name: パーツの名前
        - title: パーツのタイトル
        - temperature: パーツの現在の温度
        - max_temperature: パーツの最大許容温度
        - skin_temperature: パーツの表皮温度
        - max_skin_temperature: パーツの表皮の最大許容温度
        - thermal_percentage: パーツの温度が最大許容温度に対してどの程度の割合であるかをパーセントで表示
        """
        thermal_data = []
        for part in self.parts:
            part_data = {
                "tag": part.tag,
                "name": part.name,
                "title": part.title,
                "temperature": part.temperature,
                "max_temperature": part.max_temperature,
                "skin_temperature": part.skin_temperature,
                "max_skin_temperature": part.max_skin_temperature,
                "thermal_percentage": part.temperature / part.max_temperature * 100,
            }
            thermal_data.append(part_data)
        return thermal_data
