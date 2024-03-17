import time

import krpc_module


def main():
    # kRPCサーバーに接続
    conn = krpc_module.connect(name="Flight Status Monitor")
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
            fuel_amount = vessel.resources.amount("LiquidFuel")

            # ステータスを表示
            print(f"Altitude: {altitude:.2f}m, Speed: {speed:.2f}m/s, Fuel: {fuel_amount:.2f}")

            # 指定した間隔で情報を更新
            time.sleep(update_interval)

    except KeyboardInterrupt:
        # プログラムを終了するためのキーボード割り込み（Ctrl+C）が発生した場合
        print("Flight status monitoring stopped.")


def organize_parts(vessel):
    # 段階ごとの辞書を初期化
    stage_parts = {0: [], 1: []}  # 0段目  # 1段目

    # 0段目の部品（指定された部品）
    first_stage_parts = {
        "fairingSize1",
        "fuelTank",
        "liquidEngine3.v2",
        "probeCoreOcto2.v2",
        "batteryBankMini",
        "sasModule",
        "commDish",
        "solarPanels4",
    }

    # 1段目の部品（指定された部品）
    second_stage_parts = {
        "Decoupler.1",
        "fuelTank.long",
        "liquidEngine2.v2",
        "basicFin",
    }

    # 全ての部品を繰り返し、どちらの段階に属するかを識別
    for part in vessel.parts.all:
        # 部品の名前が0段目のリストにある場合
        if part.name in first_stage_parts:
            stage_parts[0].append(part.title)
            print(part.title)
            print(part.mass)

        # 部品の名前が1段目のリストにある場合
        elif part.name in second_stage_parts:
            stage_parts[1].append(part.title)

    return stage_parts
