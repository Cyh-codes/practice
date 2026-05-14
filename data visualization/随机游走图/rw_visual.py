import matplotlib.pyplot as plt

from random_walk import RandomWalk

# 创建一个 RandomWalk 实例
rw = RandomWalk()
rw.fill_walk()

# 绘制所有的点
plt.style.use('classic')
fig, ax = plt.subplots()
ax.scatter(rw.x_values, rw.y_values, c= rw.y_values, cmap = plt.cm.Blues, s=5)
ax.set_aspect('equal')
plt.show()