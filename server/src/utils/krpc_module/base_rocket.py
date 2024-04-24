import math
import krpc


class BaseRocket:
    def __init__(self, connection) -> None:
        """initializer"""
        self.conn = krpc.connect(name=connection)
        self.vessel = self.conn.space_center.active_vessel
        self.reference_frame = self.vessel.orbit.body.reference_frame

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

    def find_parts_by_stage(self, stage_number) -> list:
        """
        指定されたステージ番号に所属する宇宙船のパーツを検索し、リストとして返す。

        Parameters:
            stage_number (int): 検索するステージ番号

        Returns:
            list: 一致したパーツのリスト
        """
        matched_parts = [part for part in self.vessel.parts.in_stage(stage_number)]
        return matched_parts

    def find_part_by_name(self, part_name) -> list:
        """
        指定された名前に一致する宇宙船のパーツを検索し、最初に見つかったパーツを返す。
        見つからない場合はNoneを返す。

        Parameters:
            part_name (str): 検索するパーツの名前

        Returns:
            Part or None: 見つかったパーツ、または見つからなかった場合はNone
        """
        for part in self.vessel.parts.all:
            if part.name == part_name:
                return part
        return None

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
