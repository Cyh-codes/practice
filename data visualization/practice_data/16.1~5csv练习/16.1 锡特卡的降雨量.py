from pathlib import Path
import matplotlib.pyplot as plt
import csv
from datetime import datetime

# 模块级注释：该脚本用于从CSV文件读取每日天气数据，提取日期和降水量，
# 并绘制降水趋势图，最后显示图表。

# 从CSV文件中读取天气数据
path = Path('CSV解析/weather_data/sitka_weather_2021_full.csv')
# 读取文件全部内容，并按行分割成列表
lines = path.read_text().splitlines()

# 创建CSV读取器对象，遍历每一行数据
reader = csv.reader(lines)
# 读取并保存表头行（第一行）
header_row = next(reader)
print(header_row)

# 初始化两个列表，用于分别存储处理后的日期和降水量数据
dates, prcps = [], []
# 遍历CSV文件中剩余的每一行数据
for row in reader:
    # 解析当前行中的日期字符串（位于第3列，索引为2），转换为datetime对象
    date = datetime.strptime(row[2], '%Y-%m-%d')
    try:
        # 尝试解析当前行中的降水量字符串（位于第6列，索引为5）为浮点数
        prcp = float(row[5])
    except ValueError:
        # 如果转换失败，打印错误信息，便于数据质量检查
        print(f"ValueError: invalid literal for int() with base 10: '0.01' {date}")
    # 无论是否发生异常，都将日期和降水量（可能为转换失败前的值）添加到列表中
    dates.append(date)
    prcps.append(prcp)

# 设置绘图风格为 seaborn 样式（兼容性处理）
plt.style.use('seaborn-v0_8')
# 创建一个图表和坐标轴对象
fig, ax = plt.subplots()
# 在坐标轴上绘制日期-降水量的折线图
ax.plot(dates, prcps, color='blue')

# 设置图表标题，包含数据描述和地点信息
title = 'daily prcp, 2021\nSitka_full'
ax.set_title(title, fontsize=20)
# 设置x轴标签（此处为空，但保留设置以维持代码结构）
ax.set_xlabel('', fontsize=16)
# 设置y轴标签
ax.set_ylabel('PRCP ', fontsize=16)

# 显示绘制好的图表
plt.show()