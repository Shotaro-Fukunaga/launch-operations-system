import asyncio
import json

import krpc
from websockets.server import serve


def get_important_orbit_data(vessel, reference_frame):
    """
    管制チームが特に関心を持つ軌道関連のデータを収集する関数。

    :param vessel: 現在アクティブな宇宙船のオブジェクト。
    :param reference_frame: 使用する参照フレーム。
    :return: 軌道データを含む辞書。

    apoapsis_altitude: 遠地点の高度。軌道上で宇宙船が中心天体から最も遠い点の高度です。
    periapsis_altitude: 近地点の高度。軌道上で宇宙船が中心天体に最も近づく点の高度です。
    semi_major_axis: 軌道の長半径。軌道の主要な軸の長さで、軌道のサイズを示します。
    semi_minor_axis: 軌道の短半径。軌道の短い軸の長さで、軌道の形状を示します。
    period: 軌道周期。宇宙船が軌道を一周するのにかかる時間です。
    time_to_apoapsis: 次の遠地点までの時間。現在位置から遠地点に到達するまでの時間です。
    time_to_periapsis: 次の近地点までの時間。現在位置から近地点に到達するまでの時間です。
    eccentricity: 軌道の離心率。軌道が円からどれだけ逸脱しているかを示し、軌道の形状を定義します。
    inclination: 軌道の傾斜角。軌道平面が基準平面（通常は赤道面）に対して傾いている角度です。
    longitude_of_ascending_node: 昇交点の経度。軌道が基準平面を北向きに横切る点の経度です。
    argument_of_periapsis: 近地点引数。昇交点から近地点までの角度です。
    mean_anomaly_at_epoch: エポック時の平均近点角。特定時刻における宇宙船の軌道上の位置を示します。
    epoch: 軌道要素が参照する基準時刻です。
    orbital_speed: 軌道速度。宇宙船が軌道上を移動する速度です。
    next_orbit: SOI変更後の軌道。別の天体の影響下に入った後の軌道です。
    time_of_closest_approach: 他のオブジェクトに最も近づく時刻です。
    distance_at_closest_approach: 他のオブジェクトに最も近づいた時の距離です。
    true_anomaly: 真近点角。近地点からの宇宙船の位置の角度です。
    """
    orbit = vessel.orbit
    # TODO 遠点高度、近点高度の計算をする
    return {
        "apoapsis_altitude": orbit.apoapsis_altitude,
        "periapsis_altitude": orbit.periapsis_altitude,
        "semi_major_axis": orbit.semi_major_axis,
        "semi_minor_axis": orbit.semi_minor_axis,
        "period": orbit.period,
        "time_to_apoapsis": orbit.time_to_apoapsis,
        "time_to_periapsis": orbit.time_to_periapsis,
        "eccentricity": orbit.eccentricity,
        "inclination": orbit.inclination,
        "longitude_of_ascending_node": orbit.longitude_of_ascending_node,
        "argument_of_periapsis": orbit.argument_of_periapsis,
        "mean_anomaly_at_epoch": orbit.mean_anomaly_at_epoch,
        "epoch": orbit.epoch,
        # "orbital_speed": orbit.orbital_speed_at(orbit.ut),
        # "next_orbit": orbit.next_orbit if orbit.next_orbit else None,
        # "time_of_closest_approach": orbit.time_of_closest_approach(vessel) if vessel else None,
        # "distance_at_closest_approach": orbit.distance_at_closest_approach(vessel) if vessel else None,
        # "true_anomaly": orbit.true_anomaly_at_ut(orbit.ut),
    }


def get_measured_vessel_data(vessel, reference_frame):
    """
    宇宙船の直接計測可能な各種データを取得する関数。

    :param vessel: 現在アクティブな船舶のオブジェクト。
    :param reference_frame: 使用する参照フレーム。
    :return: 船舶の計測可能なデータを含む辞書。

    g_force: 現在宇宙船に作用している重力加速度の倍数です。1Gは地球の表面での重力加速度に相当します。
    mean_altitude: 宇宙船の平均海面からの高度です。海面が基準となります。
    surface_altitude: 宇宙船が現在上空を飛んでいる地表または海面からの垂直距離です。
    latitude: 宇宙船の現在位置の緯度です。赤道を基準として北または南にどれだけ離れているかを示します。
    longitude: 宇宙船の現在位置の経度です。本初子午線を基準として東または西にどれだけ離れているかを示します。
    velocity: 宇宙船の速度ベクトルです。方向と大きさ（速度）の両方を含みます。
    speed: 宇宙船の速度の大きさです。方向は考慮されません。
    horizontal_speed: 宇宙船の水平方向の速度です。地表に平行な成分のみを考慮します。
    vertical_speed: 宇宙船の垂直方向の速度です。地表に垂直な成分のみを考慮します。
    direction: 宇宙船が向いている方向です。速度ベクトルとは異なり、宇宙船の「前方」がどの方向を向いているかを示します。
    pitch: 宇宙船のピッチ角です。前後の傾きを度で示します。
    heading: 宇宙船の方位角です。北を0度とし、時計回りの角度で方向を示します。
    roll: 宇宙船のロール角です。左右の傾きを度で示します。
    dynamic_pressure: 宇宙船に作用する動的圧力です。空気の流れが生じる力の大きさをパスカルで示します。
    total_air_temperature: 宇宙船の周囲の総大気温度です。運動エネルギーによる加熱も考慮されます。
    static_air_temperature: 宇宙船の周囲の静的（周囲）大気温度です。宇宙船の運動による加熱を含みません。
    static_pressure: 宇宙船に作用する静的大気圧です。宇宙船の周囲の大気の圧力をパスカルで示します。
    drag: 宇宙船に作用する抗力です。宇宙船の進行方向に対する抵抗力を示します。
    lift: 宇宙船に作用する揚力です。宇宙船を持ち上げる力を示します。
    mach: 宇宙船の速度が音速の何倍であるかを示します。音速を1マッハとして、宇宙船の速度を相対的に示します。
    speed_of_sound: 宇宙船の周囲の大気中での音速です。温度や大気の状態に依存します。
    true_air_speed: 宇宙船の真空速度です。実際の大気中での速度を示します。
    """
    return {
        "g_force": vessel.flight().g_force,
        "mean_altitude": vessel.flight().mean_altitude,
        "surface_altitude": vessel.flight().surface_altitude,
        "latitude": vessel.flight().latitude,
        "longitude": vessel.flight().longitude,
        "velocity": vessel.flight(reference_frame).velocity,
        "speed": vessel.flight(reference_frame).speed,
        "horizontal_speed": vessel.flight(reference_frame).horizontal_speed,
        "vertical_speed": vessel.flight(reference_frame).vertical_speed,
        "direction": vessel.flight(reference_frame).direction,
        "pitch": vessel.flight().pitch,
        "heading": vessel.flight().heading,
        "roll": vessel.flight().roll,
        "total_air_temperature": vessel.flight().total_air_temperature,
        "static_air_temperature": vessel.flight().static_air_temperature,
        "dynamic_pressure": vessel.flight().dynamic_pressure,
        "static_pressure": vessel.flight().static_pressure,
        "drag": vessel.flight().drag,
        "lift": vessel.flight().lift,
        "mach": vessel.flight().mach,
        "speed_of_sound": vessel.flight().speed_of_sound,
        "true_air_speed": vessel.flight().true_air_speed,
    }


def get_calculated_vessel_data(vessel, reference_frame):
    """
    宇宙船の理論計算やシミュレーションに基づく各種データを取得する関数。

    :param vessel: 現在アクティブな船舶のオブジェクト。
    :param reference_frame: 使用する参照フレーム。
    :return: 船舶の計算に基づくデータを含む辞書。

    terrain_altitude: 宇宙船の下の地形（岩盤や地表）からの高さです。地形の起伏に依存します。
    elevation: 宇宙船が地表または海面からどの程度の高さにあるかを示します。地形に対する高さと似ていますが、こちらはより一般的な用語です。
    center_of_mass: 宇宙船の質量中心の位置です。宇宙船の重心がどこにあるかを示します。
    rotation: 宇宙船の回転を表します。空間内での宇宙船の向きを示すクォータニオンまたはオイラー角です。
    prograde: 宇宙船の順行方向です。軌道上で宇宙船が進む方向を指します。
    retrograde: 宇宙船の逆行方向です。軌道上で宇宙船が進む方向の反対を指します。
    normal: 宇宙船の軌道に垂直な方向です。軌道面に対して「上」を指します。
    anti_normal: 軌道の法線と反対の方向です。軌道面に対して「下」を指します。
    radial: 宇宙船の軌道の半径方向です。惑星中心に向かう方向を指します。
    anti_radial: 半径方向の反対です。惑星中心から離れる方向を指します。
    terminal_velocity: 宇宙船の終端速度です。抗力と重力が均衡する速度を示します。
    angle_of_attack: 宇宙船の攻撃角です。進行方向と宇宙船の向きの間の角度を示します。
    sideslip_angle: 宇宙船のスリップ角です。進行方向と宇宙船の横方向のずれを示します。
    reynolds_number: 宇宙船のレイノルズ数です。流体の流れの性質を示す無次元数です。
    aerodynamic_force: 宇宙船に作用する総空力です。揚力と抗力の合計を示します。
    static_pressure_at_msl: 平均海面での静的大気圧です。基準海面上の大気圧をパスカルで示します。
    stall_fraction: ストール（失速）の程度を示す割合です。0から1の範囲で、高い値は大規模な失速を示します。
    """
    return {
        "terrain_altitude": vessel.flight().terrain_altitude,
        "elevation": vessel.flight().elevation,
        "center_of_mass": vessel.flight(reference_frame).center_of_mass,
        "rotation": vessel.flight(reference_frame).rotation,
        "prograde": vessel.flight(reference_frame).prograde,
        "retrograde": vessel.flight(reference_frame).retrograde,
        "normal": vessel.flight(reference_frame).normal,
        "anti_normal": vessel.flight(reference_frame).anti_normal,
        "radial": vessel.flight(reference_frame).radial,
        "anti_radial": vessel.flight(reference_frame).anti_radial,
        "terminal_velocity": vessel.flight().terminal_velocity,
        "angle_of_attack": vessel.flight().angle_of_attack,
        "sideslip_angle": vessel.flight().sideslip_angle,
        # "reynolds_number": vessel.flight().reynolds_number,  # レイノルズ数,
        "aerodynamic_force": vessel.flight(reference_frame).aerodynamic_force,
        "static_pressure_at_msl": vessel.flight().static_pressure_at_msl,  # 平均海面での静的大気圧
        # "stall_fraction": vessel.flight().stall_fraction,  # ストール割合
    }


async def ksp_data(websocket, path):
    conn = krpc.connect(name="sample")
    vessel = conn.space_center.active_vessel

    # 参照フレーム。デフォルトは船舶の表面参照フレームです
    reference_frame = vessel.orbit.body.reference_frame
    while True:
        # 船舶の測定データを取得
        vessel_data = get_measured_vessel_data(vessel, reference_frame)
        # 重要な軌道データを取得
        orbit_data = get_important_orbit_data(vessel, reference_frame)

        # 二つの辞書を統合
        vessel_data.update(orbit_data)

        # 統合したデータをJSON形式でフロントエンドに送信
        await websocket.send(json.dumps(vessel_data))

        # 1秒ごとに更新
        await asyncio.sleep(0.5)


async def main():
    async with serve(ksp_data, "localhost", 8765):
        await asyncio.Future()  # このFutureは永遠に完了しない


if __name__ == "__main__":
    asyncio.run(main())
