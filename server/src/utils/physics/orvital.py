import math
# 必要なデルタVを計算するファイル


G = 6.67430e-11  # 万有引力定数 [m^3 kg^-1 s^-2]
M = 5.972e24     # 地球の質量 [kg]
R = 6371e3       # 地球の半径 [m]
h = 400e3        # 目的の高度 [m]

# 初期軌道と目的軌道の半径
r1 = R
r2 = R + h

# デルタVの計算
v1 = math.sqrt(G * M / r1)  # 初期軌道での速度
v2 = math.sqrt(G * M / r2)  # 目的軌道での速度
delta_v = v2 - v1  # 必要なデルタV

print(f"必要なデルタV: {delta_v} m/s")
