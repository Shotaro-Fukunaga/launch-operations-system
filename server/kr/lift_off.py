import kr
import time

def main():
    # kRPCサーバーに接続
    conn = kr.connect(name='Launch Program')
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

if __name__ == '__main__':
    main()
