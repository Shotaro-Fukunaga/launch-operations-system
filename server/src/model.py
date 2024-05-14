"""pydanticモジュール"""

from datetime import datetime

from pydantic import BaseModel


class TargetOrbit(BaseModel):
    """目標軌道パラメータを表すクラス

    Attributes:
        periapsis (int): 近点距離
        apoapsis (int): 遠点距離
        inclination (float): 軌道傾斜角
        speed (int): 速度
    """

    periapsis: int
    apoapsis: int
    inclination: float
    speed: int


class LaunchCommand(BaseModel):
    """ローンチコマンドを表すクラス

    Attributes:
        launch_date (datetime): ローンチ日時
        command (str): コマンド
        target_orbit (TargetOrbit): 目標軌道
    """

    launch_date: datetime
    command: str
    target_orbit: TargetOrbit
