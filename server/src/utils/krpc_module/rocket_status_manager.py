from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from src.settings.config import ACTIVE, CUTOFF, GO
from src.utils.decorators.round_output import round_output
from src.utils.krpc_module.flight_dynamics import FlightDynamics

if TYPE_CHECKING:
    from krpc.services.spacecenter import Part

    from src.utils.krpc_module.auto_pilot_manager import FlightManager
    from src.utils.krpc_module.part_unit import PartUnit

logger = logging.getLogger(__name__)


class RocketStatusManager:
    """ロケットのステータスを管理するくらす"""

    def __init__(self: RocketStatusManager, flight_manager: FlightManager) -> None:
        """Initialize the RocketStatusManager class."""
        self.vessel_manager = flight_manager.vessel_manager
        self.flight_manager = flight_manager
        self.units: list[PartUnit] = list(self.vessel_manager.units.values())
        self.flight_dynamics = FlightDynamics(self.vessel_manager.vessel)
        self.flight_info = self.vessel_manager.flight_info
        self.vessel = self.vessel_manager.vessel

    def active_check(self: RocketStatusManager, unit: PartUnit, msg: str | None = None, custom_cond: bool = True) -> None:
        """ユニットのステータスをアクティブに設定するメソッド

        指定されたユニットがアクティブ状態であるかを確認し、アクティブである場合にユニットのステータスをACTIVEに設定する

        Args:
            unit (PartUnit): チェックするユニット
            msg (str | None): ログに表示するメッセージ（デフォルトはNone）
            custom_cond (bool): カスタム条件（デフォルトはTrue）

        Returns:
            None
        """
        try:
            if unit.part and unit.status == GO and custom_cond:
                unit.status = ACTIVE
                msg = msg or f"{unit.unit_name.capitalize().replace('_', ' ')} ACTIVE"
                self.flight_manager.add_event_log(msg)
        except Exception:
            logger.exception("Error in active_check for unit %s", unit.unit_name)

    def cutoff_check(self: RocketStatusManager, unit: PartUnit, msg: str | None = None) -> None:
        """ユニットのステータスをカットオフに設定するメソッド

        指定されたユニットがカットオフ状態であるかを確認し、カットオフである場合にユニットのステータスをCUTOFFに設定する

        Args:
            unit (PartUnit): チェックするユニット
            msg (str | None): ログに表示するメッセージ（デフォルトはNone）

        Returns:
            None
        """
        try:
            if not unit.part and unit.status != CUTOFF:
                unit.status = CUTOFF
                msg = msg or f"{unit.unit_name.capitalize().replace('_', ' ')} Cutoff."
                self.flight_manager.add_event_log(msg)
        except Exception:
            logger.exception("Error in cutoff_check for unit %s", unit.unit_name)

    @round_output
    def get_rocket_status(self: RocketStatusManager) -> dict:
        """ロケットのステータスを取得するメソッド

        Returns:
            dict: ロケットの各ステージとコンポーネントのステータスを含む辞書
                - antenna (dict): アンテナのステータス
                - solar_panel_1 (dict): ソーラーパネル1のステータス
                - solar_panel_2 (dict): ソーラーパネル2のステータス
                - reaction_wheel (dict): リアクションホイールのステータス
                - satellite_bus (dict): サテライトバスのステータス
                - fairing_1 (dict): フェアリング1のステータス
                - fairing_2 (dict): フェアリング2のステータス
                - main_engine (dict): メインエンジンのステータス
                - main_tank (dict): メインタンクのステータス
                - second_engine (dict): セカンドエンジンのステータス
                - second_tank (dict): セカンドタンクのステータス
        """
        status_methods = {
            "antenna": self.get_antenna_status,
            "solar_panel_1": self.get_solar_panel_status,
            "solar_panel_2": self.get_solar_panel_status,
            "reaction_wheel": self.get_reaction_wheel_status,
            "satellite_bus": self.get_satellite_bus_status,
            "fairing_1": self.get_fairing_status,
            "fairing_2": self.get_fairing_status,
        }

        result = {name: method(name) for name, method in status_methods.items()}
        main_stage_status = self.get_main_stage_status()
        second_stage_status = self.get_second_stage_status()

        return {**result, **main_stage_status, **second_stage_status}

    @staticmethod
    def get_status_values(status: int, obj: Any, keys_defaults: dict[str, Any]) -> dict[str, int]:  # noqa: ANN401
        """オブジェクトのステータス値を取得するメソッド

        指定されたオブジェクトのキーごとの値を取得し、それらを辞書形式で返す。ステータスがCUTOFFの場合はデフォルト値を返す。

        Args:
            status (int): オブジェクトのステータス
            obj (Any): ステータス値を取得するオブジェクト
            keys_defaults (dict[str, Any]): 各キーのデフォルト値

        Returns:
            dict[str, int]: オブジェクトのステータス値を含む辞書
        """
        result = {"status": status}
        try:
            for key, default in keys_defaults.items():
                if status == CUTOFF:
                    result[key] = default
                else:
                    # 例外処理の追加
                    result[key] = getattr(obj, key, default)
        except AttributeError:
            logger.exception("AttributeError:  Setting default value for key '{%s}'", key)
            result[key] = default
        except Exception:
            logger.exception("Unexpected error: Setting default value for key '{%s}'", key)
            result[key] = default
        return result

    def get_antenna_status(self: RocketStatusManager, unit_name: str) -> dict:
        """指定されたアンテナユニットの状態情報を取得する

        Args:
            unit_name (str): アンテナユニットの名前

        Returns:
            dict: アンテナの状態に関する情報を含む辞書
                - power (float): アンテナが消費する電力
                - packet_interval (float): データパケット送信の間隔
                - packet_size (float): 送信するデータパケットのサイズ
                - packet_resource_cost (float): データパケット送信のリソースコスト
        """
        keys_defaults = {"power": 0, "packet_interval": 0, "packet_size": 0, "packet_resource_cost": 0}
        unit = self.vessel_manager.get_unit_by_name(unit_name)

        if unit and unit.part and hasattr(unit.part, "antenna"):
            return self.get_status_values(status=unit.status, obj=unit.part.antenna, keys_defaults=keys_defaults)
        return keys_defaults

    def get_solar_panel_status(self: RocketStatusManager, unit_name: str) -> dict:
        """指定されたソーラーパネルユニットの状態情報を取得する

        Args:
            unit_name (str): ソーラーパネルユニットの名前

        Returns:
            dict: ソーラーパネルの状態に関する情報を含む辞書
                - energy_flow (float): ソーラーパネルからのエネルギー流出量
                - sun_exposure (float): ソーラーパネルの太陽への露出度
        """
        keys_defaults = {"energy_flow": 0, "sun_exposure": 0}
        unit = self.vessel_manager.get_unit_by_name(unit_name)
        if unit and unit.part and hasattr(unit.part, "solar_panel"):
            self.active_check(unit=unit, custom_cond=hasattr(unit.part.solar_panel, "deployed"))
            return self.get_status_values(unit.status, unit.part.solar_panel, keys_defaults)

        return keys_defaults

    def get_reaction_wheel_status(self: RocketStatusManager, unit_name: str) -> dict:
        """指定されたリアクションホイールユニットの状態情報を取得する

        Args:
            unit_name (str): リアクションホイールユニットの名前

        Returns:
            dict: リアクションホイールの状態に関する情報を含む辞書
                - active (bool): リアクションホイールが現在アクティブかどうか
                - available_torque (tuple): 利用可能なトルクの量（ピッチ、ヨー、ロール）
                - max_torque (tuple): 最大トルクの量（ピッチ、ヨー、ロール）
        """
        unit = self.vessel_manager.get_unit_by_name(unit_name)
        keys_defaults = {"active": False, "available_torque": (0.0, 0.0, 0.0), "max_torque": (0.0, 0.0, 0.0)}
        if unit and unit.part:
            return self.get_status_values(unit.status, unit.part.reaction_wheel, keys_defaults)
        return keys_defaults

    def get_communication_status(self: RocketStatusManager) -> dict:
        """宇宙船の通信システムの状態を取得する

        Documents:
            https://krpc.github.io/krpc/python/api/space-center/comms.html#SpaceCenter.Comms

        Returns:
            - can_communicate (bool): 宇宙船が通信可能かどうかのブール値
            - can_transmit_science (bool): 科学データを送信できるかどうかのブール値
            - signal_strength (float): 現在の信号強度
            - signal_delay (float): 信号遅延時間
            - total_comm_power (float): 通信システムの合計電力
        """
        comm = self.vessel.comms
        return {
            "can_communicate": comm.can_communicate,
            "can_transmit_science": comm.can_transmit_science,
            "signal_strength": comm.signal_strength,
            "signal_delay": comm.signal_delay,
            "total_comm_power": comm.power,
        }

    def get_satellite_bus_status(self: RocketStatusManager, unit_name: str) -> dict:
        """指定されたサテライトバスユニットとその通信システムの状態情報を取得する

        Args:
            unit_name (str): サテライトバスユニットの名前

        Returns:
            dict: サテライトバスと通信システムの状態に関する情報を含む辞書
                - status (str): ユニットの状態
                - shielded (bool): ユニットがシールドされているかどうか
                - current_charge (float): 現在の電荷量
                - max_charge (float): 最大電荷容量
        """
        unit = self.vessel_manager.get_unit_by_name(unit_name)

        if unit is not None and unit.part is not None:
            self.active_check(unit, "Satellite Bus Active", not unit.part.shielded)
            bus_status = {
                "status": unit.status,
                "shielded": unit.part.shielded,
                "current_charge": unit.part.resources.amount("ElectricCharge"),
                "max_charge": unit.part.resources.max("ElectricCharge"),
            }
        else:
            bus_status = {
                "status": 0,
                "shielded": False,
                "current_charge": 0.0,
                "max_charge": 0.0,
            }

        communication_status = self.get_communication_status()
        return {**bus_status, **communication_status}

    def get_fairing_status(self: RocketStatusManager, unit_name: str) -> dict:
        """フェアリングのステータスを取得するメソッド

        Args:
            unit_name (str): フェアリングユニットの名前

        Returns:
            dict: フェアリングユニットのステータスを含む辞書
                - dynamic_pressure (float): 動的圧力
                - temperature (float): 温度
                - max_temperature (float): 最大温度
        """
        keys_defaults = {"dynamic_pressure": 0, "temperature": 0, "max_temperature": 0}
        unit = self.vessel_manager.get_unit_by_name(unit_name)
        if unit is not None:
            self.cutoff_check(unit=unit, msg="Fairing Jettisoned.")
        if unit and unit.part:
            return self.get_status_values(unit.status, unit.part, keys_defaults)
        return keys_defaults

    def get_tank_status(self: RocketStatusManager, part: Part | None, status: int) -> dict[str, Any]:
        """タンクのステータスを取得するメソッド

        Args:
            part (Part | None): チェックするタンクパーツ
            status (int): タンクのステータス

        Returns:
            dict[str, Any]: タンクパーツのステータスを含む辞書
                - status (int): タンクのステータス
                - temperature (float): 温度
                - max_temperature (float): 最大温度
                - lqd_oxygen (dict): 液体酸素の情報
                    - name (str): 液体酸素の名前
                    - amount (float): 液体酸素の量
                    - max (float): 液体酸素の最大量
                - fuel (dict): 燃料の情報
                    - name (str): 燃料の名前
                    - amount (float): 燃料の量
                    - max (float): 燃料の最大量
        """
        resource_dict = {
            "status": status,
            "temperature": 0,
            "max_temperature": 0,
            "lqd_oxygen": {"name": "", "amount": 0, "max": 0},
            "fuel": {"name": "", "amount": 0, "max": 0},
        }

        try:
            if part:
                resource_dict["temperature"] = getattr(part, "temperature", 0)
                resource_dict["max_temperature"] = getattr(part, "max_temperature", 0)

                if hasattr(part, "resources") and part.resources:
                    for resource in part.resources.all:
                        dict_key = "lqd_oxygen" if resource.name == "LqdOxygen" else "fuel"
                        resource_dict[dict_key] = {
                            "name": resource.name,
                            "amount": resource.amount,
                            "max": resource.max,
                        }
        except AttributeError:
            logger.exception("AttributeError in get_tank_status for part")
        except Exception:
            logger.exception("Unexpected error in get_tank_status")

        return resource_dict

    def get_main_stage_status(self: RocketStatusManager) -> dict:
        """mainステージの状態を取得するメソッド

        Returns:
            dict: mainエンジンとmainタンクの状態を含む辞書
                - main_engine (dict): メインエンジンのステータス
                - main_tank (dict): メインタンクのステータス
        """
        main_engine = self.vessel_manager.get_unit_by_name("main_engine")
        main_tank = self.vessel_manager.get_unit_by_name("main_tank")

        if main_engine and main_engine.part and hasattr(main_engine.part, "engine"):
            is_active = hasattr(main_engine.part.engine, "active")
            self.active_check(main_engine, f"{main_engine.unit_name.capitalize().replace('_', ' ')} Ignition", is_active)
            if main_tank:
                self.active_check(unit=main_tank, custom_cond=is_active)

        if main_engine:
            self.cutoff_check(main_engine, "MECO main engine cutoff.")
        if main_tank:
            self.cutoff_check(main_tank)

        start_mass = self.vessel.mass
        main_engine_status = self.calculate_engine_metrics(
            main_engine.part if main_engine else None,
            main_engine.status if main_engine else 0,
            start_mass,
        )
        main_tank_status = self.get_tank_status(main_tank.part if main_tank else None, main_tank.status if main_tank else 0)

        return {
            "main_engine": main_engine_status,
            "main_tank": main_tank_status,
        }

    def get_second_stage_status(self: RocketStatusManager) -> dict:
        """セカンドステージの状態を取得するメソッド

        Returns:
            dict: セカンドエンジンとセカンドタンクの状態を含む辞書
                - second_engine (dict): セカンドエンジンのステータス
                - second_tank (dict): セカンドタンクのステータス
        """
        second_engine = self.vessel_manager.get_unit_by_name("second_engine")
        second_tank = self.vessel_manager.get_unit_by_name("second_tank")

        if second_engine and second_engine.part and hasattr(second_engine.part, "engine"):
            is_active = hasattr(second_engine.part.engine, "active")
            self.active_check(second_engine, f"{second_engine.unit_name.capitalize().replace('_', ' ')} Ignition", is_active)
            if second_tank:
                self.active_check(unit=second_tank, custom_cond=is_active)
        if second_engine:
            self.cutoff_check(second_engine, "SECO second engine cutoff.")
        if second_tank:
            self.cutoff_check(second_tank)

        start_mass = self.vessel.mass

        second_engine_status = self.calculate_engine_metrics(
            second_engine.part if second_engine else None,
            second_engine.status if second_engine else 0,
            start_mass,
        )
        second_tank = self.get_tank_status(second_tank.part if second_tank else None, second_tank.status if second_tank else 0)

        return {
            "second_engine": second_engine_status,
            "second_tank": second_tank,
        }

    def calculate_engine_metrics(self: RocketStatusManager, part: Part | None, status: int, start_mass: float) -> dict:
        """エンジンのメトリクスを計算するメソッド

        Args:
            part (Part | None): 計算対象のエンジンパーツ
            status (int): エンジンのステータス
            start_mass (float): エンジンの開始質量

        Returns:
            dict: エンジンメトリクスの辞書
                - status (int): エンジンのステータス
                - start_mass (float): エンジンの開始質量
                - end_mass (float): エンジンの終了質量
                - burned_mass (float): 燃焼した質量
                - max_thrust (float): 最大推力
                - twr (float): 推力重量比 (Thrust-to-Weight Ratio)
                - slt (float): 地表レベルでの推力 (Sea Level Thrust)
                - isp (float): 比推力 (Isp)
                - atom_delta_v (float): 大気中でのデルタV
                - vac_delta_v (float): 真空中でのデルタV
                - burn_time (float): 燃焼時間
                - temperature (float): 温度
                - max_temperature (float): 最大温度
        """
        if part and hasattr(part, "engine") and part.engine:
            engine = part.engine
            thrust = engine.thrust
            max_thrust = engine.max_thrust
            temperature = part.temperature
            max_temperature = part.max_temperature
            available_thrust = engine.available_thrust
            vac_isp = engine.vacuum_specific_impulse
            current_pressure_atm = self.flight_info.static_pressure / 101325
            atom_isp = engine.specific_impulse_at(pressure=current_pressure_atm)
            fuel_mass = sum(propellant.total_resource_available for propellant in engine.propellants)
        else:
            thrust = 0
            max_thrust = 0
            temperature = 0
            max_temperature = 0
            available_thrust = 0
            vac_isp = 0
            atom_isp = 0
            fuel_mass = 0

        vac_delta_v = self.flight_dynamics.calculate_delta_v(vac_isp, fuel_mass, start_mass)
        atom_delta_v = self.flight_dynamics.calculate_delta_v(atom_isp, fuel_mass, start_mass)
        burn_time = self.flight_dynamics.burn_time_estimation(atom_isp, fuel_mass, max_thrust)
        end_mass = start_mass - fuel_mass
        twr = thrust / (start_mass * 9.81) if start_mass > 0 else 0
        slt = available_thrust / (start_mass * 9.81) if start_mass > 0 else 0

        return {
            "status": status,
            "start_mass": start_mass if part else 0,
            "end_mass": end_mass if part else 0,
            "burned_mass": fuel_mass,
            "max_thrust": max_thrust,
            "twr": twr,
            "slt": slt,
            "isp": atom_isp,
            "atom_delta_v": atom_delta_v,
            "vac_delta_v": vac_delta_v,
            "burn_time": burn_time,
            "temperature": temperature,
            "max_temperature": max_temperature,
        }
