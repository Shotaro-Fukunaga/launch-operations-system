import logging
import math
from typing import TYPE_CHECKING

from src.utils.decorators.round_output import round_output
from src.utils.krpc_module.flight_dynamics import FlightDynamics

if TYPE_CHECKING:
    from src.utils.krpc_module.vessel_manager import VesselManager


logger = logging.getLogger(__name__)


class TelemetryManager:
    """ロケットのテレメトリ情報を取得するためのクラス"""

    def __init__(self: "TelemetryManager", vessel_manager: "VesselManager") -> None:
        """Initialize the TelemetryManager class"""
        self.vessel_manager = vessel_manager
        self.orbit = self.vessel_manager.orbit
        self.vessel = self.vessel_manager.vessel
        self.flight_info = self.vessel_manager.flight_info
        self.flight_dynamics = FlightDynamics(self.vessel)

    @round_output
    def get_vessel_telemetry(self: "TelemetryManager") -> dict | None:
        """宇宙船のテレメトリ情報を返す

        Returns:
            dict:
            - surface_info (dict): 宇宙船の表面情報
            - orbit_info (dict): 宇宙船の軌道情報
            - atmosphere_info (dict): 宇宙船の大気情報
            - delta_v_info (dict): 宇宙船のデルタV情報
        """
        try:
            return {
                "surface_info": self.get_surface_info(),
                "orbit_info": self.get_orbit_info(),
                "atmosphere_info": self.get_atmosphere_info(),
                "delta_v_info": self.get_delta_v_info(),
            }
        except Exception:
            logger.exception("Failed to get vessel telemetry.")

    def get_atmosphere_info(self: "TelemetryManager") -> dict | None:
        """宇宙船の現在位置での大気情報を取得する

        Returns:
            dict:
            - angle_of_attack (float): 攻撃角
            - sideslip_angle (float): 横滑り角
            - mach (float): マッハ数
            - dynamic_pressure (float): 動的圧力
            - atmosphere_density (float): 大気密度
            - atmospheric_pressure (float): 大気圧
            - atmospheric_drag (float): 大気抵抗加速度
            - terminal_velocity (float): 終端速度
        """
        try:
            finfo = self.flight_info
            return {
                "angle_of_attack": finfo.angle_of_attack,
                "sideslip_angle": finfo.sideslip_angle,
                "mach": finfo.mach,
                "dynamic_pressure": finfo.dynamic_pressure,
                "atmosphere_density": finfo.atmosphere_density,
                "atmospheric_pressure": finfo.static_pressure,
                "atmospheric_drag": self.flight_dynamics.calculate_atmospheric_drag_acceleration(),
                "terminal_velocity": finfo.terminal_velocity,
            }
        except Exception:
            logger.exception("Failed to get atmosphere info.")

    def get_orbit_info(self: "TelemetryManager") -> dict | None:
        """宇宙船の軌道に関する情報を取得する

        Returns:
            dict:
            - orbital_speed (float): 軌道速度
            - apoapsis_altitude (float): 遠地点の高度
            - periapsis_altitude (float): 近地点の高度
            - period (float): 軌道周期
            - time_to_apoapsis (float): 遠地点までの時間
            - time_to_periapsis (float): 近地点までの時間
            - semi_major_axis (float): 長半径
            - inclination (float): 軌道傾斜角
            - eccentricity (float): 軌道離心率
            - longitude_of_ascending_node (float): 昇交点の経度
            - argument_of_periapsis (float): 近点引数
            - prograde (float): 前進方向のベクトル
        """
        try:
            orbit = self.orbit
            return {
                "orbital_speed": orbit.speed,
                "apoapsis_altitude": orbit.apoapsis_altitude,
                "periapsis_altitude": orbit.periapsis_altitude,
                "period": orbit.period,
                "time_to_apoapsis": orbit.time_to_apoapsis,
                "time_to_periapsis": orbit.time_to_periapsis,
                "semi_major_axis": orbit.semi_major_axis,
                "inclination": math.degrees(orbit.inclination),
                "eccentricity": orbit.eccentricity,
                "longitude_of_ascending_node": orbit.longitude_of_ascending_node,
                "argument_of_periapsis": orbit.argument_of_periapsis,
                "prograde": self.flight_info.prograde,
            }
        except Exception:
            logger.exception("Failed to get orbit info.")

    def get_surface_info(self: "TelemetryManager") -> dict | None:
        """宇宙船が現在接触している表面の情報を取得する

        Returns:
            dict:
            - altitude_als (float): 平均海面高度
            - altitude_true (float): 実際の表面高度
            - pitch (float): ピッチ角
            - heading (float): 進行方向
            - roll (float): ロール角
            - surface_speed (float): 表面速度
            - vertical_speed (float): 垂直速度
            - surface_horizontal_speed (float): 水平面速度
            - latitude (float): 緯度
            - longitude (float): 経度
            - biome (str): バイオーム
            - situation (VesselSituation): 宇宙船の状況
        """
        try:
            finfo = self.flight_info
            return {
                "altitude_als": finfo.mean_altitude,
                "altitude_true": finfo.surface_altitude,
                "pitch": finfo.pitch,
                "heading": finfo.heading,
                "roll": finfo.roll,
                "surface_speed": finfo.speed,
                "vertical_speed": finfo.vertical_speed,
                "surface_horizontal_speed": finfo.horizontal_speed,
                "latitude": finfo.latitude,
                "longitude": finfo.longitude,
                "biome": self.vessel.biome,
                "situation": str(self.vessel.situation),
            }
        except Exception:
            logger.exception("Failed to get surface info.")

    def get_engine_status(self: "TelemetryManager", unit_name: str) -> dict:
        """エンジンのステータスを取得する

        Args:
            unit_name (str): ユニット名

        Returns:
            dict:
            - thrust (float): 推力
            - available_thrust (float): 利用可能な推力
            - max_thrust (float): 最大推力
            - max_vacuum_thrust (float): 最大真空推力
            - temperature (float): 温度
            - max_temperature (float): 最大温度
            - thrust_limit (float): 推力制限
            - isp (float): 比推力
            - specific_impulse_at (float): 特定の圧力での比推力
            - vacuum_specific_impulse (float): 真空中の比推力
            - propellant_mass (float): 推進剤の質量
            - propellant_names (list[str]): 推進剤の名前リスト
            - propellant_ratios (dict): 推進剤の比率
            - throttle (float): スロットル
        """
        unit = self.vessel_manager.get_unit_by_name(unit_name)
        engine = None if not unit or not unit.part or not hasattr(unit.part, "engine") or not unit.part.engine else unit.part.engine
        current_pressure = self.flight_info.static_pressure
        current_pressure_atm = current_pressure / 101325
        return {
            "thrust": getattr(engine, "thrust", 0),
            "available_thrust": getattr(engine, "available_thrust", 0),
            "max_thrust": getattr(engine, "max_thrust", 0),
            "max_vacuum_thrust": getattr(engine, "max_vacuum_thrust", 0),
            "temperature": getattr(engine, "temperature", 0),
            "max_temperature": getattr(engine, "max_temperature", 0),
            "thrust_limit": getattr(engine, "thrust_limit", 0),
            "isp": getattr(engine, "isp", 0),
            "specific_impulse_at": engine.specific_impulse_at(pressure=current_pressure_atm)
            if engine and engine.specific_impulse_at
            else 0,
            "vacuum_specific_impulse": getattr(engine, "vacuum_specific_impulse", 0),
            "propellant_mass": sum(propellant.total_resource_available for propellant in engine.propellants)
            if engine and engine.propellants
            else 0,
            "propellant_names": getattr(engine, "propellant_names", []),
            "propellant_ratios": getattr(engine, "propellant_ratios", {}),
            "throttle": getattr(engine, "throttle", 0),
        }

    # TODO: DRYじゃないのでリファクタリングする
    def calculate_delta_v_info(self: "TelemetryManager", engines: list[dict], stages_start_mass: list[float]) -> dict | None:
        """デルタV情報を計算する

        Args:
            engines (list[dict]): エンジンの情報リスト
            stages_start_mass (list[float]): 各ステージのスタート質量リスト

        Returns:
            dict:
            - stage_delta_v_atom (float): 最後のステージの大気中でのデルタV
            - stage_delta_v_vac (float): 最後のステージの真空中でのデルタV
            - total_delta_v_atom (float): 全ステージの大気中での合計デルタV
            - total_delta_v_vac (float): 全ステージの真空中での合計デルタV
            - delta_v_list (list[dict]): 各エンジンごとのデルタV計算結果を含むリスト
        """
        delta_v_list = []

        for i, engine in enumerate(engines):
            start_mass = stages_start_mass[min(i, len(stages_start_mass) - 1)]
            vac_isp = engine["vacuum_specific_impulse"]
            atom_isp = engine["specific_impulse_at"]
            fuel_mass = engine["propellant_mass"]
            vac_delta_v = self.flight_dynamics.calculate_delta_v(vac_isp, fuel_mass, start_mass)
            atom_delta_v = self.flight_dynamics.calculate_delta_v(atom_isp, fuel_mass, start_mass)
            burn_time = self.flight_dynamics.burn_time_estimation(atom_isp, fuel_mass, engine["max_thrust"])

            delta_v_list.append(
                {
                    "start_mass": start_mass,
                    "end_mass": start_mass - fuel_mass,
                    "burned_mass": fuel_mass,
                    "max_thrust": engine["max_thrust"],
                    "twr": engine["thrust"] / (start_mass * 9.81),
                    "slt": engine["available_thrust"] / (start_mass * 9.81),
                    "isp": atom_isp,
                    "atom_delta_v": atom_delta_v,
                    "vac_delta_v": vac_delta_v,
                    "time": burn_time,
                },
            )

        # 全ステージの合計デルタVを計算
        total_delta_v_atom = sum(stage["atom_delta_v"] for stage in delta_v_list)
        total_delta_v_vac = sum(stage["vac_delta_v"] for stage in delta_v_list)

        # 最後のステージのデルタV
        stage_delta_v_atom = delta_v_list[-1]["atom_delta_v"] if delta_v_list else 0
        stage_delta_v_vac = delta_v_list[-1]["vac_delta_v"] if delta_v_list else 0

        return {
            "stage_delta_v_atom": stage_delta_v_atom,
            "stage_delta_v_vac": stage_delta_v_vac,
            "total_delta_v_atom": total_delta_v_atom,
            "total_delta_v_vac": total_delta_v_vac,
            "delta_v_list": delta_v_list,
        }

    def get_delta_v_info(self: "TelemetryManager") -> dict | None:
        """ロケットのデルタVステータスを返す

        Returns:
        - stage_delta_v_atom (float): 最後のステージの大気中でのデルタV
        - stage_delta_v_vac (float): 最後のステージの真空中でのデルタV
        - total_delta_v_atom (float): 全ステージの大気中での合計デルタV
        - total_delta_v_vac (float): 全ステージの真空中での合計デルタV
        - delta_v_list (list[dict]): 各エンジンごとのデルタV計算結果を含むリスト
        """
        try:
            main_engine_status = self.get_engine_status("main_engine")
            second_engine_status = self.get_engine_status("second_engine")

            start_mass = self.vessel_manager.vessel.mass
            stages_start_mass = [start_mass, start_mass]

            engines = [second_engine_status, main_engine_status]

            return self.calculate_delta_v_info(engines, stages_start_mass)
        except Exception:
            logger.exception("Failed to get delta v info.")
