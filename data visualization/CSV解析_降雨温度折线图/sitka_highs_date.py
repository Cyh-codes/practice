from pathlib import Path
import csv 
import matplotlib.pyplot as plt
from datetime import datetime

path = Path('weather_data/sitka_weather_07-2021_simple.csv')
lines = path.read_text().splitlines()

reader = csv.reader(lines)
header_row = next(reader)

# 提取日期和最高温度
dates, highs= [], []
for row in reader:
    current_date = datetime.strptime(row[2], '%Y-%m-%d')
    high = int(row[4])
    dates.append(current_date)
    highs.append(high)

# 绘制数据绘图
plt.style.use('seaborn-v0_8')
fig, ax= plt.subplots()
ax.plot(dates, highs, color='red')

# 设置绘图格式
ax.set_title('Daily High Temperatures, July 2021', fontsize=24)
ax.set_xlabel('', fontsize=14)
fig.autofmt_xdate()
ax.set_ylabel('Temperatures (F)', fontsize=14)
ax.tick_params(labelsize=16)

plt.show()