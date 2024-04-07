
import krpc

import math
KRPC_CONNECT_SERVER_NAME = "Find Parts By Tag"

class RocketStage:
    def __init__(self, parts):
        self.parts = parts

    @property
    def mass(self):
        """ステージの全パーツの質量の合計を返す"""
        return sum(part.mass for part in self.parts)
    
    @property
    def dry_mass(self):
        """ステージの全パーツの乾燥質量の合計を返す"""
        return sum(part.dry_mass for part in self.parts)


class RocketTelemetory:
    def __init__(self):
        self.conn = krpc.connect(name=KRPC_CONNECT_SERVER_NAME)
        self.vessel = self.conn.space_center.active_vessel
        self.reference_frame= self.vessel.orbit.body.reference_frame
        # パーツ関係のドキュメント：https://krpc.github.io/krpc/python/api/space-center/parts.html
        self.payload = RocketStage(self._find_parts_by_tag("payload"))  # ペイロード
        self.first_stage = RocketStage(self._find_parts_by_tag("first_stage")) # 一段目
        self.second_stage = RocketStage(self._find_parts_by_tag("second_stage"))  # 二段目
        self.launch_clamps = RocketStage(self._find_parts_by_tag("launch_clamp"))  # 発射装置


        self.g_earth = 9.81  # 地球の重力加速度（m/s²）
         

    def _find_parts_by_tag(self,tag_name):
        # タグ名に一致するパーツを検索
        matched_parts = [part for part in self.vessel.parts.all if part.tag == tag_name]
        return matched_parts
    
    
    def _find_parts_by_stage(self, stage_number):
        # ステージ番号に一致するパーツを検索
        matched_parts = [part for part in self.vessel.parts.in_stage(stage_number)]
        return matched_parts
    


    def calculate_atmospheric_drag(self):
        """
        大気抵抗を計算する

        大気抵抗力の公式：
            F_d = 0.5 * ρ * v^2 * A * Cd

            F_d は大気抵抗の力（ニュートン、N）
            ρ は大気密度（キログラム毎立方メートル、kg/m^3）
            v は物体の速度（メートル毎秒、m/s）
            A は物体が抵抗を受ける表面積（平方メートル、m^2）
            Cd は抗力係数（無次元）です

        :return: 大気抵抗の力（ニュートン単位）
        """
        vessel = self.vessel.flight(self.vessel.orbit.body.reference_frame)
        # Cd：抗力係数（Ferram Aerospace Researchから取得）
        drag_coefficient = vessel.drag_coefficient
        # ρ：大気密度を取得
        air_density = vessel.atmosphere_density
        # v：速度を取得（空対地速度）
        speed = vessel.speed
        # A：抗力が作用する面積（A）MOD FARのRef Areaを参照
        area = 5.917
        # F_d：大気抵抗力を計算
        drag_force = 0.5 * air_density * speed**2 * area * drag_coefficient
        
        return drag_force   
    
    
    def calculate_atmospheric_drag_acceleration(self):
        """
        大気抵抗による加速度を計算する関数。
        
        :param vessel: kRPCで取得した現在の船体オブジェクト
        :return: 大気抵抗による加速度 [m/s^2]
        """
        vessel = self.vessel
        # 現在の船体の質量を取得
        mass = vessel.mass 
        # 大気抵抗による加速度を計算
        drag_acceleration = self.calculate_atmospheric_drag() / mass
        return drag_acceleration
    
    
    def calculate_delta_v(self,isp, fuel_mass,m0 = 0):
        # 宇宙船の現在の総質量を取得
        # 地球の重力加速度（m/s²）
        g0 = 9.80665  # m/s²
        # 燃料を消費した後の質量（kg）
        mf = m0 - fuel_mass
        # Delta-Vの計算
        delta_v = isp * g0 * math.log(m0 / mf)
        return delta_v
    

    def burn_time_estimation(self,isp, fuel_mass,available_thrust):
        # 地球の重力加速度（m/s²）
        g0 = 9.80665  # m/s²
        # エンジンの推力（ニュートン）
        thrust = available_thrust
        # 燃料消費率（kg/s）
        fuel_consumption_rate = thrust / (isp * g0)
        # 燃焼時間の見積もり
        burn_time_estimation = fuel_mass / fuel_consumption_rate
        return burn_time_estimation
    
       
    
    # https://krpc.github.io/krpc/python/api/space-center/parts.html#SpaceCenter.Engine
    def get_all_engines_status(self):
        # TODO 一旦完成：後で数値のチェックと後日docstringを追加
        """宇宙船のすべてのエンジンの基本ステータスを返す"""
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
                "propellants": engine.propellants,
                "throttle": engine.throttle,
            }
            engines_status.append(status) 

        return engines_status




    def get_atmosphere_info(self):
        # TODO 一旦完成：後で数値のチェックと後日docstringを追加
        flight_info = self.vessel.flight(self.reference_frame)
        return {
            "angle_of_attack":flight_info.angle_of_attack,
            "sideslip_angle":flight_info.sideslip_angle,
            "mach":flight_info.mach,
            "dynamic_pressure":flight_info.dynamic_pressure,
            "atmosphere_density":flight_info.atmosphere_density,
            "atmospheric_pressure":flight_info.static_pressure,
            "atmospheric_drag":self.calculate_atmospheric_drag_acceleration(),
            "terminal_velocity":flight_info.terminal_velocity
        }
    
    def get_orbit_info(self):
        # TODO 一旦完成：後で数値のチェックと後日docstringを追加
        orbit = self.vessel.orbit
        flight_info = self.vessel.flight(self.reference_frame)
        return{
            "orbital_speed":orbit.orbital_speed_at(),
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
            "prograde":flight_info.prograde,
        }
    
    
    def get_surface_info(self):
        # TODO 一旦完成：後で数値のチェックと後日docstringを追加
        flight_info = self.vessel.flight(self.reference_frame)
        return {
            # 海面高度
            "altitude_als":flight_info.mean_altitude,
            "altitude_true":flight_info.surface_altitude,
            "pitch":flight_info.pitch,
            "heading":flight_info.heading,
            "roll":flight_info.roll,
            "surface_speed":flight_info.speed,
            "vertical_speed":flight_info.vertical_speed,
            "surface_horizontal_speed":flight_info.horizontal_speed,
            "latitude":flight_info.latitude,#緯度
            "longitude":flight_info.longitude,#経度
            "biome":self.vessel.biome,
            "situation":self.vessel.situation
        }
    

    def get_delta_v_status(self):
        """
        Calculate and return the delta V status of the rocket.

        SLT（Sea Level Thrust-to-Weight Ratio）
        """

        payload_mass = self.payload.mass
        first_stage_mass = self.first_stage.mass
        second_stage_mass = self.second_stage.mass
        
        stages_start_mass = [
            payload_mass + first_stage_mass,  # 第1ステージのスタート質量
            payload_mass + first_stage_mass + second_stage_mass  # 第2ステージのスタート質量
        ]

        engines = self.get_all_engines_status()

        delta_v_list = []

        for i, engine in enumerate(engines):
            start_mass = stages_start_mass[min(i, len(stages_start_mass)-1)]
            max_vac_thrust = engine["max_vacuum_thrust"]
            max_thrust = engine["max_thrust"]
            fuel_mass = sum(propellant.total_resource_available for propellant in engine["propellants"])
            vac_isp = engine["vacuum_specific_impulse"]
            atom_isp = engine["specific_impulse_at"]
            slt = max_thrust / (start_mass  * 9.81)
            twr = max_vac_thrust / (start_mass  * 9.81)
            vac_delta_v = self.calculate_delta_v(vac_isp, fuel_mass, start_mass)
            atom_delta_v = self.calculate_delta_v(atom_isp, fuel_mass, start_mass)
            burn_time = self.burn_time_estimation(atom_isp, fuel_mass,max_thrust)
            end_mass = start_mass - fuel_mass

            delta_v_list.append({
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
                "time": burn_time
            }  )
        
        # Calculate the total delta V for atom and vac
        total_delta_v_atom = sum([stage['atom_delta_v'] for stage in delta_v_list])
        total_delta_v_vac = sum([stage['vac_delta_v'] for stage in delta_v_list])

        # Calculate the stage delta V for atom and vac
        stage_delta_v_atom = delta_v_list[-1]['atom_delta_v'] if delta_v_list else 0
        stage_delta_v_vac = delta_v_list[-1]['vac_delta_v'] if delta_v_list else 0

        return {
            "stage_delta_v_atom": stage_delta_v_atom,
            "stage_delta_v_vac": stage_delta_v_vac,
            "total_delta_v_atom": total_delta_v_atom,
            "total_delta_v_vac": total_delta_v_vac,
            "delta_v_list": delta_v_list
        }


    # TODO 温度を返す関数

    # TODO 上昇statusを返す関数

    # TODO 機体情報を保存する関数

    # TODO 予定軌道ルートを返す関数

