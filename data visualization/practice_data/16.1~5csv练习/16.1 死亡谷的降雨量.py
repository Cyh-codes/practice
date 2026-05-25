from pathlib import Path  # 用于处理文件路径的模块
import matplotlib.pyplot as plt  # 用于绘图的模块
import csv  # 用于解析CSV文件的模块
from datetime import datetime  # 用于日期时间转换的模块

# 定义要解析的CSV文件路径（包含天气数据）
path = Path('CSV解析/weather_data/death_valley_2021_full.csv')
# 读取文件内容并按行分割，获取所有行数据
lines = path.read_text().splitlines()

# 创建CSV读取器对象，用于逐行解析数据
reader = csv.reader(lines)
# 获取CSV文件的标题行（第一行），用于了解数据列含义
header_row = next(reader)
print(header_row)  # 打印标题行，便于查看数据列

# 初始化两个列表，分别用于存储日期和降水数据
dates, prcps = [], []
# 遍历CSV中的每一行数据（从第二行开始）
for row in reader:
    # 从每行的第三列（索引2）提取日期字符串，并转换为datetime对象
    date = datetime.strptime(row[2], '%Y-%m-%d')
    try:
        # 尝试将第四列（索引3）的降水数据转换为浮点数
        prcp = float(row[3])
    except ValueError:
        # 如果转换失败（例如数据为空），则执行此块：跳过该日数据，打印提示信息
        print(f"缺失降水数据，已安全跳过该日: {date}")
        
    else:
        # 只有当try块中的float()转换成功时，才会执行此块：将有效数据添加到列表中
        dates.append(date)
        prcps.append(prcp)

# 设置绘图风格为'seaborn-v0_8'（一种美观的样式）
plt.style.use('seaborn-v0_8')
# 创建一个图形和坐标轴对象
fig, ax = plt.subplots()
# 在坐标轴上绘制日期与降水数据的折线图，线条颜色为蓝色
ax.plot(dates, prcps, color='blue')
# 设置图表标题，包含年份和地点信息
title = 'daily prcp, 2021\nDeath_valley_full'
ax.set_title(title, fontsize=20)
# 设置X轴标签（此处留空，因为日期已自动标注）
ax.set_xlabel('', fontsize=16)
# 设置Y轴标签为降水（PRCP），字体大小为16
ax.set_ylabel('PRCP ', fontsize=16)

# 显示绘制好的图表
plt.show()