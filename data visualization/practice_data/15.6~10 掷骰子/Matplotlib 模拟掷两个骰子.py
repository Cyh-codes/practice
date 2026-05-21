import random
import matplotlib.pyplot as plt

class Die:
    """表示一个骰子的类。"""
    def __init__(self, num_sides=6):
        self.num_sides = num_sides

    def roll(self):
        """返回一个1到骰子面数的随机值。"""
        return random.randint(1, self.num_sides)

# 1. 创建两个 6 面的骰子
die_1 = Die()
die_2 = Die()

# 2. 掷骰子多次，并存储结果
num_rolls = 50000
results = []
for roll_num in range(num_rolls):
    result = die_1.roll() + die_2.roll()
    results.append(result)

# 3. 分析结果：统计每个点数出现的次数
max_result = die_1.num_sides + die_2.num_sides
frequencies = []
poss_results = range(2, max_result + 1)

for value in poss_results:
    frequency = results.count(value)
    frequencies.append(frequency)

# 4. 使用 Matplotlib 可视化结果
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制柱状图，设置颜色和边缘线
bars = ax.bar(poss_results, frequencies, color='skyblue', edgecolor='black', alpha=0.8)

# 设置标题和标签
ax.set_title(f"Simulation of Rolling Two D6 Dies {num_rolls} Times (Matplotlib)", fontsize=16)
ax.set_xlabel("Result (Sum of Two Dies)", fontsize=12)
ax.set_ylabel("Frequency of Result", fontsize=12)

# 强制 X 轴刻度显示 2 到 12 的每一个整数
ax.set_xticks(poss_results)

# 在每个柱子上方添加具体的数值标签（边缘情况优化：避免数据肉眼难辨）
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),  # 纵向偏移3个像素
                textcoords="offset points",
                ha='center', va='bottom', fontsize=9)

# 开启网格线（只显示 Y 轴方向，辅助对齐）
ax.grid(axis='y', linestyle='--', alpha=0.5)

# 显示图表
plt.tight_layout()
plt.show()