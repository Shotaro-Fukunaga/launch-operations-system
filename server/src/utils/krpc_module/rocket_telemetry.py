from .rocket_base import BaseRocket


class RocketTelemetry(BaseRocket):
    """ロケットのテレメトリ情報を取得するためのクラス"""
    def __init__(self, krpc_connect_server_name: str, rocket_part_list: list[dict]) -> None:
        """initializer"""
        super().__init__(krpc_connect_server_name, rocket_part_list)

    def get_all_engines_status(self):
        """宇宙船のすべてのエンジンの基本ステータス情報を取得する

        Documents:
            https://krpc.github.io/krpc/python/api/space-center/parts.html#SpaceCenter.Engine

        Returns:
            list[dict]: すべてのエンジンのステータス情報を含むリスト
                dict:
                - tag (str): エンジンパーツに関連付けられたタグ
                - stage (int): エンジンのステージ番号
                - name (str): エンジンパーツの名前
                - active (bool): エンジンが現在アクティブかどうかを示すブール値
                - thrust (float): エンジンの現在の推力（ニュートン単位）
                - available_thrust (float): 現在利用可能な推力
                - available_thrust_at (float): 現在の大気圧における利用可能な推力
                - max_thrust (float): エンジンの最大推力
                - max_thrust_at (float): 現在の大気圧での最大推力
                - max_vacuum_thrust (float): 真空中での最大推力
                - thrust_limit (float): 推力制限（パーセンテージ）
                - isp (float): エンジンの比推力
                - specific_impulse_at (float): 現在の大気圧での比推力
                - vacuum_specific_impulse (float): 真空中の比推力
                - propellant_names (list[str]): 使用する推進剤の名前
                - propellant_ratios (dict[str, float]): 推進剤の比率
                - propellants (List[Propellant]): エンジンに使用される推進剤の詳細
                - throttle (float): 現在のスロットル位置（パーセンテージ）
                - temperature (float): パーツの現在の温度
                - max_temperature (float): パーツの最大許容温度
                - skin_temperature (float): パーツの表面温度
                - max_skin_temperature (float): パーツの表面の最大許容温度
        """
        engines_status = []  # すべてのエンジンのステータス情報を保持するリスト

        for engine in self.vessel.parts.engines:
            current_pressure = self.vessel.flight().static_pressure  # 現在の大気圧（パスカル）
            # パスカルからアトモスフィアに変換（1アトモスフィア = 101325 パスカル）
            current_pressure_atm = current_pressure / 101325

            status = {
                "tag": engine.part.tag,
                "stage": engine.part.stage,
                "name": engine.part.name,
                "active": engine.active,
                "thrust": engine.thrust,
                "available_thrust": engine.available_thrust,
                "available_thrust_at": engine.available_thrust_at(pressure=current_pressure_atm),
                "max_thrust": engine.max_thrust,
                "max_thrust_at": engine.max_thrust_at(pressure=current_pressure_atm),
                "max_vacuum_thrust": engine.max_vacuum_thrust,
                "thrust_limit": engine.thrust_limit,
                "isp": engine.specific_impulse,
                "specific_impulse_at": engine.specific_impulse_at(pressure=current_pressure_atm),
                "vacuum_specific_impulse": engine.vacuum_specific_impulse,
                "propellant_names": engine.propellant_names,
                "propellant_ratios": engine.propellant_ratios,
                # ref: https://krpc.github.io/krpc/python/api/space-center/parts.html#SpaceCenter.Propellant
                "propellants": engine.propellants,
                "throttle": engine.throttle,
                "temperature": engine.part.temperature,
                "max_temperature": engine.part.max_temperature,
                "skin_temperature": engine.part.skin_temperature,
                "max_skin_temperature": engine.part.max_skin_temperature,
            }
            engines_status.append(status)
        return engines_status

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
        unit = self.get_unit_by_name(unit_name)
        return {
            "state": unit.part.antenna.state,
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
        unit = self.get_unit_by_name(unit_name)
        return {
            "state": unit.part.solar_panel.state,
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
        unit = self.get_unit_by_name(unit_name)
        return {
            "active": unit.part.reaction_wheel.active,
            "available_torque": unit.part.reaction_wheel.available_torque,
            "max_torque": unit.part.reaction_wheel.max_torque,
        }

    def get_satellite_bus_status(self, unit_name: str):
        """
        指定されたサテライトバスユニットの状態情報を取得する

        Args:
            unit_name (str): サテライトバスユニットの名前

        Returns:
            dict: サテライトバスの状態に関する情報を含む辞書
                - shielded (bool): ユニットがシールドされているかどうか
                - current_charge (float): 現在の電荷量
                - max_charge (float): 最大電荷容量
        """
        unit = self.get_unit_by_name(unit_name)
        return {
            "shielded": unit.part.shielded,
            "current_charge": unit.part.resources.amount("ElectricCharge"),
            "max_charge": unit.part.resources.max("ElectricCharge"),
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
        flight_info = self.vessel.flight(self.reference_frame)
        return {
            "angle_of_attack": flight_info.angle_of_attack,
            "sideslip_angle": flight_info.sideslip_angle,
            "mach": flight_info.mach,
            "dynamic_pressure": flight_info.dynamic_pressure,
            "atmosphere_density": flight_info.atmosphere_density,
            "atmospheric_pressure": flight_info.static_pressure,
            "atmospheric_drag": self.calculate_atmospheric_drag_acceleration(),
            "terminal_velocity": flight_info.terminal_velocity,
        }

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
        orbit = self.vessel.orbit
        flight_info = self.vessel.flight(self.reference_frame)

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
        flight_info = self.vessel.flight(self.reference_frame)
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
            "biome": self.vessel.biome,
            "situation": str(self.vessel.situation),
        }

    def get_delta_v_status(self):
        """
        ロケットのデルタVステータスを返す

        Returns:
        - stage_delta_v_atom (float): 最後のステージの大気中でのデルタV
        - stage_delta_v_vac (float): 最後のステージの真空中でのデルタV
        - total_delta_v_atom (float): 全ステージの大気中での合計デルタV
        - total_delta_v_vac (float): 全ステージの真空中での合計デルタV
        - delta_v_list (list[dict]): 各エンジンごとのデルタV計算結果を含むリスト
            dict:
            - stage (int): エンジンのステージ番号
            - start_mass (float): ステージ開始時の質量
            - end_mass (float): ステージ終了時の質量
            - burned_mass (float): 燃焼した燃料の質量
            - max_thrust (float): 最大真空推力
            - twr (float): 推力重量比（真空中）
            - slt (float): 海面推力重量比
            - isp (float): 大気中での比推力
            - atom_delta_v (float): 大気中でのデルタV
            - vac_delta_v (float): 真空中でのデルタV
            - time (float): 燃焼時間
        """

        payload_mass = self.total_mass_by_group("payload_stage")
        first_stage_mass = self.total_mass_by_group("first_stage")
        second_stage_mass = self.total_mass_by_group("second_stage")

        stages_start_mass = [
            payload_mass + second_stage_mass,  # セカンドステージのスタート質量
            payload_mass + first_stage_mass + second_stage_mass,  # メインステージのスタート質量
        ]

        engines = self.get_all_engines_status()

        delta_v_list = []

        for i, engine in enumerate(engines):
            start_mass = stages_start_mass[min(i, len(stages_start_mass) - 1)]
            max_vac_thrust = engine["max_vacuum_thrust"]
            max_thrust = engine["max_thrust"]
            fuel_mass = sum(propellant.total_resource_available for propellant in engine["propellants"])
            vac_isp = engine["vacuum_specific_impulse"]
            atom_isp = engine["specific_impulse_at"]
            slt = max_thrust / (start_mass * 9.81)
            twr = max_vac_thrust / (start_mass * 9.81)
            vac_delta_v = self.calculate_delta_v(vac_isp, fuel_mass, start_mass)
            atom_delta_v = self.calculate_delta_v(atom_isp, fuel_mass, start_mass)
            burn_time = self.burn_time_estimation(atom_isp, fuel_mass, max_thrust)
            end_mass = start_mass - fuel_mass

            delta_v_list.append(
                {
                    "stage": engine["stage"],
                    "start_mass": start_mass,
                    "end_mass": end_mass,
                    "burned_mass": fuel_mass,
                    "max_thrust": max_vac_thrust,
                    "twr": twr,
                    "slt": slt,
                    "isp": atom_isp,
                    "atom_delta_v": atom_delta_v,
                    "vac_delta_v": vac_delta_v,
                    "time": burn_time,
                }
            )

        # Calculate the total delta V for atom and vac
        total_delta_v_atom = sum([stage["atom_delta_v"] for stage in delta_v_list])
        total_delta_v_vac = sum([stage["vac_delta_v"] for stage in delta_v_list])

        # Calculate the stage delta V for atom and vac
        stage_delta_v_atom = delta_v_list[-1]["atom_delta_v"] if delta_v_list else 0
        stage_delta_v_vac = delta_v_list[-1]["vac_delta_v"] if delta_v_list else 0

        return {
            "stage_delta_v_atom": stage_delta_v_atom,
            "stage_delta_v_vac": stage_delta_v_vac,
            "total_delta_v_atom": total_delta_v_atom,
            "total_delta_v_vac": total_delta_v_vac,
            "delta_v_list": delta_v_list,
        }

    def get_fuel_status(self):
        main_tank = self.get_unit_by_name("main_tank")
        second_tank = self.get_unit_by_name("second_tank")

        return {
            "main_tank": main_tank.get_fuel_status(),
            "second_tank": second_tank.get_fuel_status(),
        }

    def get_thermal_status(self):
        """ロケット各ステージの熱関連データを返す

        Returns:
            dict: 各ユニットの熱関連に関する情報を含む辞書
            - tag (str): パーツに割り当てられたタグ
            - name (str): パーツの名前
            - title (str): パーツのタイトル
            - temperature (float): パーツの現在の温度
            - max_temperature (float): パーツの最大許容温度
            - skin_temperature (float): パーツの表皮温度
            - max_skin_temperature (float): パーツの表皮の最大許容温度
            - thermal_percentage (float): パーツの温度が最大許容温度に対してどの程度の割合であるかをパーセントで表示
        """
        satellite_bus_unit = self.get_unit_by_name("satellite_bus")
        fairing_unit = self.get_unit_by_name("fairing")
        second_tank_unit = self.get_unit_by_name("second_tank")
        second_engine_unit = self.get_unit_by_name("second_engine")
        main_tank_unit = self.get_unit_by_name("main_tank")
        main_engine_unit = self.get_unit_by_name("main_engine")

        return {
            "satellite_bus": satellite_bus_unit.get_temperature(),
            "fairing": fairing_unit.get_temperature(),
            "second_tank": second_tank_unit.get_temperature(),
            "second_engine": second_engine_unit.get_temperature(),
            "main_tank": main_tank_unit.get_temperature(),
            "main_engine": main_engine_unit.get_temperature(),
        }

    def get_payload_status(self):
        """
        ペイロードステージに関連する部品の重量と状態情報を取得する

        Returns:
            dict: ペイロードステージの総質量と各ペイロード部品の詳細情報を含む
                - payload_mass (float): ペイロードステージの総質量
                - anttena (dict): アンテナの現在の状態に関する詳細情報
                - satellite_bus (dict): サテライトバスの状態に関する詳細情報
                - solar_panel_1 (dict): 最初のソーラーパネルの状態に関する詳細情報
                - solar_panel_2 (dict): 二番目のソーラーパネルの状態に関する詳細情報
                - reaction_wheel (dict): リアクションホイールの状態に関する詳細情報
        """
        return {
            "payload_mass": self.total_mass_by_group("payload_stage"),
            "anttena": self.get_antenna_status("anttena"),
            "satellite_bus": self.get_satellite_bus_status("satellite_bus"),
            "solar_panel_1": self.get_solar_panel_status("solar_panel_1"),
            "solar_panel_2": self.get_solar_panel_status("solar_panel_2"),
            "reaction_wheel": self.get_reaction_wheel_status("reaction_wheel"),
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
