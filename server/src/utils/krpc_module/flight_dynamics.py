import math
from krpc.services.spacecenter import Vessel


class FlightDynamics:
    """宇宙飛行の動力学に関連する計算をまとめたクラス"""

    def __init__(self: "FlightDynamics", vessel: Vessel):
        self.vessel = vessel

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
        # 初期質量が0以下、比推力が0以下、燃料質量が0以下、または消費後の質量が0以下の場合、デルタVは計算できない
        if m0 <= 0 or isp <= 0 or fuel_mass <= 0 or (m0 - fuel_mass) <= 0:
            return 0
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
        g0 = 9.80665  # 地球の重力加速度（m/s²）
        # 比推力、推力、または燃料質量が0以下の場合、燃焼時間は計算できない
        if isp <= 0 or available_thrust <= 0 or fuel_mass <= 0:
            return 0

        # エンジンの推力（ニュートン）
        thrust = available_thrust
        # 燃料消費率（kg/s）
        fuel_consumption_rate = thrust / (isp * g0)
        # 燃焼時間の見積もり
        burn_time_estimation = fuel_mass / fuel_consumption_rate
        return burn_time_estimation
