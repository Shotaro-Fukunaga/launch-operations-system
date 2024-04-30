import math
import krpc
import datetime
import time
from src.utils.krpc_module.rocket_unit import Unit


class RocketCore:
    """ロケットの基本クラス"""
    _instance = None

    def __new__(cls, connection, rocket_schema_list):
        if cls._instance is None:
            cls._instance = super(RocketCore, cls).__new__(cls)
        cls._instance.initialize(connection, rocket_schema_list)
        return cls._instance

    def initialize(self, connection, rocket_schema_list):
        # Initialization only if data is updated or instance is uninitialized
        if not hasattr(self, 'is_initialized') or self.rocket_schema_list != rocket_schema_list:
            self.conn = krpc.connect(name=connection)
            self.vessel = self.conn.space_center.active_vessel
            self.orbit = self.vessel.orbit
            self.reference_frame = self.vessel.orbit.body.reference_frame
            self.flight_info = self.vessel.flight(self.reference_frame)
            self.units = {part["tag"]: Unit(vessel=self.vessel, **part) for part in rocket_schema_list}
            self.rocket_schema_list = rocket_schema_list  # Store the schema list for comparison
            self.is_initialized = True


    def calculate_atmospheric_drag(self) -> float:
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

    def calculate_atmospheric_drag_acceleration(self) -> float:
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

    def calculate_delta_v(self, isp, fuel_mass, m0) -> float:
        """宇宙船のデルタVを計算する
        デルタVは宇宙船が持つ速度変更の能力を示し、宇宙飛行での軌道変更やマヌーバに必要な燃料の量を評価するために使用される

        デルタVは以下のロケット方程式に基づいて計算される:
            Δv = Isp * g0 * ln(m0 / mf)

        Ispは比推力（秒）
        g0は地球の重力加速度（m/s²）
        m0は燃料を含む初期質量（kg）
        mfは燃料を消費した後の質量（kg）

        Parameters:
            isp (float): エンジンの比推力（秒）
            fuel_mass (float): 使用する燃料の質量（kg）
            m0 (float): 初期の総質量（kg）

        Returns:
            float: 計算されたデルタV（m/s）
        """

        g0 = 9.80665  # 地球の重力加速度（m/s²）
        mf = m0 - fuel_mass  # 燃料を消費した後の質量（kg）
        delta_v = isp * g0 * math.log(m0 / mf)  # Delta-Vの計算
        return delta_v

    def burn_time_estimation(self, isp, fuel_mass, available_thrust) -> float:
        """エンジンの燃焼時間を見積もる
        指定された推力と比推力で、指定された燃料を消費するのに必要な時間を計算する

        燃焼時間の式:
            burn_time = fuel_mass / fuel_consumption_rate

        燃料消費率の式:
            fuel_consumption_rate = thrust / (isp * g0)


        g0は地球の重力加速度（m/s²）で、ispは比推力（秒）
        thrustはエンジンの推力（ニュートン）

        Parameters:
            isp (float): エンジンの比推力（秒）
            fuel_mass (float): 燃料の質量（kg）
            available_thrust (float): 利用可能な推力（ニュートン）

        Returns:
            float: 推定される燃焼時間（秒）
        """
        # 地球の重力加速度（m/s²）
        g0 = 9.80665  # m/s²
        # エンジンの推力（ニュートン）
        thrust = available_thrust
        # 燃料消費率（kg/s）
        fuel_consumption_rate = thrust / (isp * g0)
        # 燃焼時間の見積もり
        burn_time_estimation = fuel_mass / fuel_consumption_rate
        return burn_time_estimation

    def total_mass_by_group(self, group_name) -> float:
        """
        指定されたグループ名に属する全ユニットの総質量を計算する

        Args:
            group_name (str): 質量を計算するユニットのグループ名

        Returns:
            float: 指定されたグループに属するユニットの総質量
        """
        total_mass = 0
        for unit in self.units.values():
            if unit.group_name == group_name:
                total_mass += getattr(unit.part, "mass", 0)
        return total_mass

    def get_unit_group_name(self, group_name) -> list:
        """
        指定されたグループ名に一致するユニットのリストを返す

        Args:
            group_name (str): 取得するユニットのグループ名

        Returns:
            list: 指定されたグループ名に一致するユニットオブジェクトのリスト
        """
        unit_list = []
        for unit in self.units.values():
            if unit.group_name == group_name:
                unit_list.append(unit)
        return unit_list

    def get_unit_by_name(self, unit_name) -> Unit:
        """
        指定されたユニット名に一致する最初のユニットを返す

        Args:
            unit_name (str): 検索するユニットの名前

        Returns:
            Unit: 指定された名前に一致するユニットオブジェクト。一致するユニットがない場合は None
        """
        for unit in self.units.values():
            if unit.unit_name == unit_name:
                return unit
        return None

    def get_all_unit_status(self) -> dict:
        """
        登録されている全ユニットのステータスを返す

        Returns:
            dict: 各ユニット名をキーとし、そのステータスを値とする辞書
        """
        return {unit.unit_name: unit.status for unit in self.units.values()}

    def find_parts_by_tag(self, tag_name) -> list:
        """
        指定されたタグ名に一致する宇宙船のパーツを検索し、リストとして返す

        Parameters:
            tag_name (str): 検索するパーツのタグ名

        Returns:
            list: 一致したパーツのリスト
        """
        matched_parts = [part for part in self.vessel.parts.all if part.tag == tag_name]
        return matched_parts
