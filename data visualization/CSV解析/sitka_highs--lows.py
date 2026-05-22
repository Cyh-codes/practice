from pathlib import Path
import csv 
import matplotlib.pyplot as plt
from datetime import datetime
# 给每天最高温度~最低温度  范围
path = Path('weather_data/sitka_weather_2021_simple.csv')
lines = path.read_text().splitlines()

reader = csv.reader(lines)
header_row = next(reader)

dates, highs, lows = [], [], []
for row in reader:
    current_time = datetime.strptime(row[2], '%Y-%m-%d')
    high = int(row[4])
    low = int(row[5])
    dates.append(current_time)
    highs.append(high)
    lows.append(low)

plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots()
ax.plot(dates, highs, color='red', alpha=0.5)
ax.plot(dates, lows, color='blue', alpha=0.5)
# alpha 设置颜色透明度 0是完全透明 1是完全不透明
plt.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1)

ax.set_title('Year High Temperatures  and  Low Temperatures, 2021', fontsize=24)
ax.set_xlabel('', fontsize=16)
ax.set_ylabel('Temperature (F)', fontsize=16)

ax.tick_params(labelsize=16)

plt.show()