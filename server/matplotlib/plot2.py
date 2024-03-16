import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Figureを追加
fig = plt.figure(figsize=(8, 8))

# 3DAxesを追加
ax = fig.add_subplot(111, projection='3d')

# Axesのタイトルを設定
ax.set_title("Small Sphere", size=20)

# 軸ラベルを設定
ax.set_xlabel("x", size=14)
ax.set_ylabel("y", size=14)
ax.set_zlabel("z", size=14)

# 軸目盛を設定
ax.set_xticks([-1.0, -0.5, 0.0, 0.5, 1.0])
ax.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0])

# 球体の中心座標と半径
sphere_center = [0, 0, 0]
sphere_radius = 0.1

# 球体を作成し、3D軸に追加
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x_sphere = sphere_radius * np.outer(np.cos(u), np.sin(v)) + sphere_center[0]
y_sphere = sphere_radius * np.outer(np.sin(u), np.sin(v)) + sphere_center[1]
z_sphere = sphere_radius * np.outer(np.ones(np.size(u)), np.cos(v)) + sphere_center[2]

# 球体を描画
ax.plot_surface(x_sphere, y_sphere, z_sphere, color='b')

plt.show()
