from pathlib import Path
import matplotlib.pyplot as plt
import csv 
from datetime import datetime

path = Path('weather_data/death_valley_2021_simple.csv')
lines = path.read_text().splitlines()

reader = csv.reader(lines)
header_row = next(reader)

dates, highs, lows = [], [], []
for row in reader:
    # Traceback (most recent call last):
    # File "d:\Github\data visualization\CSV解析\death_valley_highd_lows.py", line 15, in <module>
    #  high = int(row[3])
    # ValueError: invalid literal for int() with base 10: ''
    # 最高温度那里缺失但没有异常处理
    current_date = datetime.strptime(row[2], '%Y-%m-%d')
    try:
        #  加上异常处理会自动跳过没有数据的情况
        high = int(row[3])
        low = int(row[4])
    except ValueError:
        print(f"Missing data for {current_date}")
    dates.append(current_date)
    highs.append(high)
    lows.append(low)

plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots()
ax.plot(dates, highs, color='red', alpha=0.5)
ax.plot(dates, lows, color='blue', alpha=0.5)
# alpha 设置颜色透明度 0是完全透明 1是完全不透明
plt.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1)

title = 'daily high and low temperatures, 2021\nDeath Valley, CA'
ax.set_title(title, fontsize=20)
ax.set_xlabel('', fontsize=16)
ax.set_ylabel('Temperature (F)', fontsize=16)

plt.show()