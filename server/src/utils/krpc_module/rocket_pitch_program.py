# ロケットの移動プログラム


import time

import krpc_module


def main():
    # kRPCサーバーに接続
    conn = krpc_module.connect(name="Launch Program")
    vessel = conn.space_center.active_vessel

    # SASを有効にする
    vessel.control.sas = True
    time.sleep(1)  # SASが有効になるのを少し待つ

    # スロットルを全開に設定
    vessel.control.throttle = 1.0

    # エンジンを起動（リフトオフ）
    vessel.control.activate_next_stage()

    # 一定の高度に達するまで待機（例: 10000メートル）
    while vessel.flight().mean_altitude < 10000:
        time.sleep(1)  # 1秒ごとに高度をチェック

    # スロットルをオフにしてエンジンを停止
    vessel.control.throttle = 0.0
    print("Reached 10000 meters altitude, engines stopped.")


def main2():
    # kRPCサーバーに接続
    conn = krpc_module.connect(name="Pitch Adjustment")
    vessel = conn.space_center.active_vessel

    # スロットルを最大に設定し、リフトオフ
    vessel.control.throttle = 1.0
    vessel.control.sas = True
    time.sleep(1)  # 少し待ってからエンジンを起動
    vessel.control.activate_next_stage()

    # 高度が10kmに達するまで待機
    while vessel.flight().mean_altitude < 10000:
        time.sleep(1)  # CPU使用率を抑えるためにウェイトを入れる

    # 自動操縦を有効にし、SASを無効にする
    vessel.auto_pilot.engage()
    vessel.control.sas = False
    time.sleep(0.4)  # AutoPilotが安定するまで待つ

    # 高度10kmで船首を45度、方位角を90度（東向き）に設定
    vessel.auto_pilot.target_pitch_and_heading(45, 90)

    # 例: 高度が20kmに達したら2段目のロケットを切り離す
    while vessel.flight().mean_altitude < 20000:
        time.sleep(1)  # CPU使用率を抑えるためにウェイトを入れる

    # vessel.control.throttle = 0.0
    # 2段目のロケットを切り離し（次のステージをアクティブにする）
    vessel.auto_pilot.disengage()
    vessel.control.sas = True
    time.sleep(1)
    vessel.control.activate_next_stage()
    # vessel.auto_pilot.target_pitch_and_heading(45, 90)
    # vessel.control.throttle = 100.0

    # # アポアプシスが70kmに達するまで待機
    # while vessel.orbit.apoapsis_altitude < 70000:
    #     time.sleep(0.1)  # 小さなウェイトを入れて、ポーリング間隔を設定

    # # アポアプシスが70kmに達したらスロットルを0に設定
    # vessel.control.throttle = 0

    while vessel.flight().mean_altitude < 70000:
        time.sleep(0.1)

    vessel.auto_pilot.target_pitch_and_heading(0, 90)

    while vessel.orbit.speed < 2700:
        time.sleep(0.1)

    vessel.control.throttle = 0.0

    vessel.auto_pilot.disengage()


def main3():
    # kRPCサーバーに接続
    conn = krpc_module.connect(name="sample")
    vessel = conn.space_center.active_vessel

    # 現在の軌道情報を取得
    orbit = vessel.orbit
    mu = orbit.body.gravitational_parameter
    r = orbit.apoapsis

    # 目的の軌道に必要なデルタVを計算（この部分は例示的なもので、具体的な計算が必要です）
    delta_v = 100  # Δvの値を適宜調整してください

    # マヌーバーノードを追加（ここでは、現在時刻から10秒後に設定）
    node_time = conn.space_center.ut + 10
    node = vessel.control.add_node(node_time, prograde=delta_v)

    # マヌーバー実行までの待機
    time_to_node = node.time_to - (vessel.control.nodes[0].remaining_burn_vector(node.reference_frame)[1] / 2)
    time.sleep(time_to_node)

    # マヌーバー実行（エンジン噴射）
    vessel.control.throttle = 1.0
    time.sleep(vessel.control.nodes[0].remaining_burn_vector(node.reference_frame)[1])  # 実際の噴射時間に合わせて調整
    vessel.control.throttle = 0.0

    # マヌーバーノードを削除
    node.remove()
