import kr
import time

def main():
    # kRPCサーバーに接続
    conn = kr.connect(name='Flight Status Monitor')
    vessel = conn.space_center.active_vessel

    # ロケットのステータスを監視する間隔（秒）
    update_interval = 1

    try:
        while True:
            # 現在の高度を取得
            altitude = vessel.flight().mean_altitude
            # 現在の速度を取得
            speed = vessel.flight(vessel.orbit.body.reference_frame).speed
            # 燃料残量を取得
            fuel_amount = vessel.resources.amount('LiquidFuel')

            # ステータスを表示
            print(f"Altitude: {altitude:.2f}m, Speed: {speed:.2f}m/s, Fuel: {fuel_amount:.2f}")

            # 指定した間隔で情報を更新
            time.sleep(update_interval)

    except KeyboardInterrupt:
        # プログラムを終了するためのキーボード割り込み（Ctrl+C）が発生した場合
        print("Flight status monitoring stopped.")

if __name__ == '__main__':
    main()
