# 実行方法
# このスクリプトをrocket_pitch_adjust.pyという名前で保存します。
# KSPを起動し、kRPCサーバーを有効にして宇宙船を準備します。
# Python環境で上記のスクリプトを実行します。これにより、自動的にリフトオフが行われ、高度10km時点で船首が45度になるようにピッチが調整されます。

import kr
import time

def main():
    # kRPCサーバーに接続
    conn = kr.connect(name='Pitch Adjustment')
    vessel = conn.space_center.active_vessel

    # スロットルを最大に設定し、リフトオフ
    vessel.control.throttle = 1.0
    vessel.control.sas=True
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

if __name__ == '__main__':
    main()