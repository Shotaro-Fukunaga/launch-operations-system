from typing import TYPE_CHECKING
import logging
from src.utils.decorators.round_output import round_output
from src.utils.krpc_module.flight_dynamics import FlightDynamics

if TYPE_CHECKING:
    from src.utils.krpc_module.vessel_manager import VesselManager


logger = logging.getLogger(__name__)

class TelemetryManager:
    """ロケットのテレメトリ情報を取得するためのクラス"""

    def __init__(self, vessel_manager: "VesselManager") -> None:
        """initializer"""
        self.vessel_manager = vessel_manager
        self.orbit = self.vessel_manager.orbit
        self.vessel = self.vessel_manager.vessel
        self.flight_info = self.vessel_manager.flight_info
        self.flight_dynamics = FlightDynamics(self.vessel)

    @round_output
    def get_rocket_status(self):
        """
        宇宙船の各コンポーネントのステータスを取得し、それらを辞書形式で返す。

        Returns:
            dict: 各コンポーネントのステータスを含む辞書。
        """
        status_methods = {
            "antenna": self.get_antenna_status,
            "fairing_1": self.get_fairing_status,
            "fairing_2": self.get_fairing_status,
            "main_tank": self.get_tank_status,
            "second_tank": self.get_tank_status,
            "main_engine": self.get_delta_v_status,
            "second_engine": self.get_delta_v_status,
            "solar_panel_1": self.get_solar_panel_status,
            "solar_panel_2": self.get_solar_panel_status,
            "reaction_wheel": self.get_reaction_wheel_status,
            "satellite_bus": self.get_satellite_bus_status,
        }

        result = {name: method(name) for name, method in status_methods.items()}

        return result

    @round_output
    def get_vessel_telemetry(self):
        return {
            "surface_info": self.get_surface_info(),
            "orbit_info": self.get_orbit_info(),
            "atmosphere_info": self.get_atmosphere_info(),
            "delta_v_info": self.get_delta_v_info(),
        }

    def get_fairing_status(self, unit_name: str):
        unit = self.vessel_manager.get_unit_by_name(unit_name)
        if unit.part is not None and hasattr(unit.part, "dynamic_pressure"):
            dynamic_pressure = unit.part.dynamic_pressure
        else:
            dynamic_pressure = 0

        data = {
            "status": unit.status,
            "dynamic_pressure": dynamic_pressure,
            "temperature": getattr(unit.part, "temperature", 0) if unit.part else 0,
            "max_temperature": getattr(unit.part, "max_temperature", 0) if unit.part else 0,
        }
        return data

    def get_engine_status(self, unit_name: str):
        unit = self.vessel_manager.get_unit_by_name(unit_name)

        if not unit or not unit.part or not hasattr(unit.part, "engine") or not unit.part.engine:
            engine = None  # エンジンが存在しない場合はNoneで扱う
        else:
            engine = unit.part.engine
        current_pressure = self.flight_info.static_pressure
        current_pressure_atm = current_pressure / 101325
        data = {
            "status": unit.status,
            "thrust": getattr(engine, "thrust", 0),
            "available_thrust": getattr(engine, "available_thrust", 0),
            "max_thrust": getattr(engine, "max_thrust", 0),
            "max_vacuum_thrust": getattr(engine, "max_vacuum_thrust", 0),
            "temperature": getattr(engine, "temperature", 0),
            "max_temperature": getattr(engine, "max_temperature", 0),
            "thrust_limit": getattr(engine, "thrust_limit", 0),
            "isp": getattr(engine, "isp", 0),
            "specific_impulse_at": engine.specific_impulse_at(pressure=current_pressure_atm) if engine and engine.specific_impulse_at else 0,
            "vacuum_specific_impulse": getattr(engine, "vacuum_specific_impulse", 0),
            "propellant_mass": sum(propellant.total_resource_available for propellant in engine.propellants) if engine and engine.propellants else 0,
            "propellant_names": getattr(engine, "propellant_names", []),
            "propellant_ratios": getattr(engine, "propellant_ratios", {}),
            "throttle": getattr(engine, "throttle", 0),
        }
        return data

    def get_tank_status(self, unit_name: str) -> dict[dict]:

        unit = self.vessel_manager.get_unit_by_name(unit_name)
        if not unit or not unit.part:
            return {}

        resource_dict = {
            "status": unit.status,
            "temperature": getattr(unit.part, "temperature", 0),
            "max_temperature": getattr(unit.part, "max_temperature", 0),
        }
        resources = unit.part.resources.all

        for resource in resources:
            dict_key = "lqd_oxygen" if resource.name == "LqdOxygen" else "fuel"
            resource_dict[dict_key] = {
                "name": getattr(resource, "name", ""),
                "amount": getattr(resource, "amount", 0),
                "max": getattr(resource, "max", 0),
            }

        return resource_dict

    def get_antenna_status(self, unit_name: str):
        """
        指定されたアンテナユニットの状態情報を取得する

        Args:
            unit_name (str): アンテナユニットの名前

        Returns:
            dict: アンテナの状態に関する情報を含む辞書
                - state (str): アンテナの現在の状態
                - power (float): アンテナが消費する電力
                - packet_interval (float): データパケット送信の間隔
                - packet_size (float): 送信するデータパケットのサイズ
                - packet_resource_cost (float): データパケット送信のリソースコスト
        """
        unit = self.vessel_manager.get_unit_by_name(unit_name)
        return {
            "status": unit.status,
            "power": unit.part.antenna.power,
            "packet_interval": unit.part.antenna.packet_interval,
            "packet_size": unit.part.antenna.packet_size,
            "packet_resource_cost": unit.part.antenna.packet_resource_cost,
        }

    def get_solar_panel_status(self, unit_name: str):
        """
        指定されたソーラーパネルユニットの状態情報を取得する

        Args:
            unit_name (str): ソーラーパネルユニットの名前

        Returns:
            dict: ソーラーパネルの状態に関する情報を含む辞書
                - state (str): ソーラーパネルの現在の状態
                - energy_flow (float): ソーラーパネルからのエネルギー流出量
                - sun_exposure (float): ソーラーパネルの太陽への露出度
        """
        unit = self.vessel_manager.get_unit_by_name(unit_name)
        return {
            "status": unit.status,
            "energy_flow": unit.part.solar_panel.energy_flow,
            "sun_exposure": unit.part.solar_panel.sun_exposure,
        }

    def get_reaction_wheel_status(self, unit_name: str):
        """
        指定されたリアクションホイールユニットの状態情報を取得する

        Args:
            unit_name (str): リアクションホイールユニットの名前

        Returns:
            dict: リアクションホイールの状態に関する情報を含む辞書
                - active (bool): リアクションホイールが現在アクティブかどうか
                - available_torque (tuple): 利用可能なトルクの量（ピッチ、ヨー、ロール）
                - max_torque (tuple): 最大トルクの量（ピッチ、ヨー、ロール）
        """
        unit = self.vessel_manager.get_unit_by_name(unit_name)
        return {
            "status": unit.status,
            "active": unit.part.reaction_wheel.active,
            "available_torque": unit.part.reaction_wheel.available_torque,
            "max_torque": unit.part.reaction_wheel.max_torque,
        }

    def get_communication_status(self):
        """宇宙船の通信システムの状態を取得する

        Documents:
            https://krpc.github.io/krpc/python/api/space-center/comms.html#SpaceCenter.Comms

        Returns:
            - can_communicate (bool): 宇宙船が通信可能かどうかのブール値
            - can_transmit_science (bool): 科学データを送信できるかどうかのブール値
            - signal_strength (float): 現在の信号強度
            - signal_delay (float): 信号遅延時間
            - total_comm_power (float): 通信システムの合計電力
            - control_path (list[dict]): 通信経路に関する情報のリスト
                dict:
                - type (str): リンクタイプ（'home', 'control', 'relay'）
                - signal_strength (float): リンクの信号強度

        """
        comm = self.vessel.comms
        control_path_info = []
        for link in comm.control_path:
            link_info = {
                "type": link.type.name,
                "signal_strength": link.signal_strength,
            }
            control_path_info.append(link_info)

        return {
            "can_communicate": comm.can_communicate,
            "can_transmit_science": comm.can_transmit_science,
            "signal_strength": comm.signal_strength,
            "signal_delay": comm.signal_delay,
            "total_comm_power": comm.power,
            "control_path": control_path_info,
        }

    def get_satellite_bus_status(self, unit_name: str):
        """
        指定されたサテライトバスユニットとその通信システムの状態情報を取得する

        Args:
            unit_name (str): サテライトバスユニットの名前

        Returns:
            dict: サテライトバスと通信システムの状態に関する情報を含む辞書
                - status (str): ユニットの状態
                - shielded (bool): ユニットがシールドされているかどうか
                - current_charge (float): 現在の電荷量
                - max_charge (float): 最大電荷容量
                - can_communicate (bool): 宇宙船が通信可能かどうか
                - can_transmit_science (bool): 科学データを送信できるかどうか
                - signal_strength (float): 現在の信号強度
                - signal_delay (float): 信号遅延時間
                - total_comm_power (float): 通信システムの合計電力
                - control_path (list[dict]): 通信経路に関する情報のリスト
        """
        unit = self.vessel_manager.get_unit_by_name(unit_name)

        bus_status = {
            "status": unit.status,
            "shielded": unit.part.shielded,
            "current_charge": unit.part.resources.amount("ElectricCharge"),
            "max_charge": unit.part.resources.max("ElectricCharge"),
        }

        # 通信システムの状態を取得する
        communication_status = self.get_communication_status()

        # 両方の辞書をマージして返す
        return {**bus_status, **communication_status}

    def get_delta_v_status(self, unit_name: str):
        """
        指定されたエンジンのデルタVステータスを計算して返す。

        Args:
            engine_name (str): 'main_engine' または 'second_engine' のいずれかのエンジン名

        Returns:
            dict: 指定エンジンのデルタV情報を含む辞書
        """
        engine_status = self.get_engine_status(unit_name)
        payload_mass = self.vessel_manager.get_total_mass_by_group("payload_stage")
        first_stage_mass = self.vessel_manager.get_total_mass_by_group("first_stage")
        second_stage_mass = self.vessel_manager.get_total_mass_by_group("second_stage")

        if unit_name == "main_engine":
            start_mass = payload_mass + first_stage_mass + second_stage_mass
        elif unit_name == "second_engine":
            start_mass = payload_mass + second_stage_mass
        else:
            raise ValueError("Invalid engine name provided. Use 'main_engine' or 'second_engine'.")

        vac_isp = engine_status["vacuum_specific_impulse"]
        atom_isp = engine_status["specific_impulse_at"]
        fuel_mass = engine_status["propellant_mass"]
        vac_delta_v = self.flight_dynamics.calculate_delta_v(vac_isp, fuel_mass, start_mass)
        atom_delta_v = self.flight_dynamics.calculate_delta_v(atom_isp, fuel_mass, start_mass)
        burn_time = self.flight_dynamics.burn_time_estimation(atom_isp, fuel_mass, engine_status["max_thrust"])

        delta_v_info = {
            "status": engine_status["status"],
            "start_mass": start_mass,
            "end_mass": start_mass - fuel_mass,
            "burned_mass": fuel_mass,
            "max_thrust": engine_status["max_thrust"],
            "twr": engine_status["thrust"] / (start_mass * 9.81),
            "slt": engine_status["available_thrust"] / (start_mass * 9.81),
            "isp": atom_isp,
            "atom_delta_v": atom_delta_v,
            "vac_delta_v": vac_delta_v,
            "burn_time": burn_time,
            "temperature": engine_status["max_temperature"],
            "max_temperature": engine_status["max_temperature"],
        }

        return delta_v_info

    ###########################################################################

    def get_delta_v_info(self):
        """
        ロケットのデルタVステータスを返す

        Returns:
        - stage_delta_v_atom (float): 最後のステージの大気中でのデルタV
        - stage_delta_v_vac (float): 最後のステージの真空中でのデルタV
        - total_delta_v_atom (float): 全ステージの大気中での合計デルタV
        - total_delta_v_vac (float): 全ステージの真空中での合計デルタV
        - delta_v_list (list[dict]): 各エンジンごとのデルタV計算結果を含むリスト
        """

        main_engine_status = self.get_engine_status("main_engine")
        second_engine_status = self.get_engine_status("second_engine")
        payload_mass = self.vessel_manager.get_total_mass_by_group("payload_stage")
        first_stage_mass = self.vessel_manager.get_total_mass_by_group("first_stage")
        second_stage_mass = self.vessel_manager.get_total_mass_by_group("second_stage")

        stages_start_mass = [
            payload_mass + second_stage_mass,  # セカンドステージのスタート質量
            payload_mass + first_stage_mass + second_stage_mass,  # メインステージのスタート質量
        ]

        engines = [second_engine_status, main_engine_status]

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
                }
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

    def get_atmosphere_info(self):
        """宇宙船の現在位置での大気情報を取得する

        Returns:
            dict:
            - angle_of_attack (float): 攻撃角
            - sideslip_angle (float): 横滑り角
            - mach (float): マッハ数
            - dynamic_pressure (float): 動的圧力
            - atmosphere_density (float): 大気密度
            - atmospheric_pressure (float): 大気圧
            - atmospheric_drag (float): 大気抵抗加速度（自己計算）
            - terminal_velocity (float): 終端速度
        """
        try:
            flight_info = self.flight_info
            return {
                "angle_of_attack": flight_info.angle_of_attack,
                "sideslip_angle": flight_info.sideslip_angle,
                "mach": flight_info.mach,
                "dynamic_pressure": flight_info.dynamic_pressure,
                "atmosphere_density": flight_info.atmosphere_density,
                "atmospheric_pressure": flight_info.static_pressure,
                "atmospheric_drag": self.flight_dynamics.calculate_atmospheric_drag_acceleration(),
                "terminal_velocity": flight_info.terminal_velocity,
            }
        except Exception:
            logger.exception("Failed to get atmosphere info.")

    def get_orbit_info(self):
        """
        宇宙船の軌道に関する情報を取得する

        Returns:
            dict:
            - orbital_speed (float): 軌道速度
            - apoapsis_altitude (float): アポアプシス（遠地点）の高度
            - periapsis_altitude (float): ペリアプシス（近地点）の高度
            - period (float): 軌道周期
            - time_to_apoapsis (float): アポアプシス（遠地点）までの時間
            - time_to_periapsis (float): ペリアプシス（近地点）までの時間
            - semi_major_axis (float): 長半径
            - inclination (float): 軌道傾斜角
            - eccentricity (float): 軌道離心率
            - longitude_of_ascending_node (float): 昇交点の経度
            - argument_of_periapsis (float): 近点引数
            - prograde (float): 前進方向のベクトル
        """
        orbit = self.orbit
        flight_info = self.flight_info

        return {
            "orbital_speed": orbit.speed,
            "apoapsis_altitude": orbit.apoapsis_altitude,
            "periapsis_altitude": orbit.periapsis_altitude,
            "period": orbit.period,
            "time_to_apoapsis": orbit.time_to_apoapsis,
            "time_to_periapsis": orbit.time_to_periapsis,
            "semi_major_axis": orbit.semi_major_axis,
            "inclination": orbit.inclination,
            "eccentricity": orbit.eccentricity,
            "longitude_of_ascending_node": orbit.longitude_of_ascending_node,
            "argument_of_periapsis": orbit.argument_of_periapsis,
            "prograde": flight_info.prograde,
        }

    def get_surface_info(self):
        """
        宇宙船が現在接触している表面の情報を取得する

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
        flight_info = self.flight_info
        vessel = self.vessel
        return {
            "altitude_als": flight_info.mean_altitude,
            "altitude_true": flight_info.surface_altitude,
            "pitch": flight_info.pitch,
            "heading": flight_info.heading,
            "roll": flight_info.roll,
            "surface_speed": flight_info.speed,
            "vertical_speed": flight_info.vertical_speed,
            "surface_horizontal_speed": flight_info.horizontal_speed,
            "latitude": flight_info.latitude,
            "longitude": flight_info.longitude,
            "biome": vessel.biome,
            "situation": str(vessel.situation),
        }
