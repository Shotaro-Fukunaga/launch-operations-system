# Import Python Modules
import numpy as np # 数値計算ライブラリ
from scipy.integrate import odeint # 常微分方程式を解くライブラリ
import matplotlib.pyplot as plt # 描画ライブラリ

# 二体問題の運動方程式
def func(x, t):
    GM = 398600.4354360959 # 地球の重力定数, km3/s2
    r = np.linalg.norm(x[0:3])
    dxdt = [x[3],
            x[4],
            x[5],
            -GM*x[0]/(r**3),
            -GM*x[1]/(r**3),
            -GM*x[2]/(r**3)]
    return dxdt 

# 微分方程式の初期条件
# 物体が地球から10,000kmの高さにあり、y方向に7km/sの速度で運動を開始する状態を表します。これは一種の軌道を示す初期条件です。
# 初期位置
initial_x = 10000  # 地球からの高さ（km）
initial_y = 0      # y方向の初期位置
initial_z = 0      # z方向の初期位置

# 初期速度
initial_vx = 0    # x方向の初期速度
initial_vy = 7    # y方向の初期速度（7km/s）
initial_vz = 0    # z方向の初期速度

# 初期条件配列
x0 = [initial_x, initial_y, initial_z, initial_vx, initial_vy, initial_vz]# 位置(x,y,z)＋速度(vx,vy,vz)
t  = np.linspace(0, 86400, 1000) # 1日分 軌道伝播

# 微分方程式の数値計算
sol = odeint(func, x0, t)


# 描画
plt.plot(sol[:, 0],sol[:, 1], 'b')
plt.grid() # 格子をつける
plt.gca().set_aspect('equal') # グラフのアスペクト比を揃える
plt.show()