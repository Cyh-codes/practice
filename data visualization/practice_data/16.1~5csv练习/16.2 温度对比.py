from pathlib import Path
import matplotlib.pyplot as plt
import csv 
from datetime import datetime

path1 = Path('CSV解析/weather_data/sitka_weather_2021_full.csv')
lines1 = path1.read_text().splitlines()

reader1 = csv.reader(lines1)
header_row1 = next(reader1)

path2 = Path('CSV解析/weather_data/death_valley_2021_full.csv')
lines2 = path2.read_text().splitlines()

reader2 = csv.reader(lines2)
header_row2 = next(reader2)
dates1, highs1, lows1 = [], [], []
dates2, highs2, lows2 = [], [], []

for row in reader1:
    date = datetime.strptime(row[2], '%Y-%m-%d')
    try:
        high = int(row[7])
        low = int(row[8])
    except ValueError:
        print(f"ValueError: invalid literal for int() with base 10:'' {date}")
    else:
        dates1.append(date)
        highs1.append(high)
        lows1.append(low)

for row in reader2:
    date = datetime.strptime(row[2], '%Y-%m-%d')
    try:
        high = int(row[6])
        low = int(row[7])
    except ValueError:
        print(f"ValueError: invalid literal for int() with base 10:'' {date}")
    else:
        dates2.append(date)
        highs2.append(high)
        lows2.append(low)

plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots()

ax.plot(dates1, highs1, color='blue', alpha=0.5)
ax.plot(dates1, lows1, color='blue', alpha=0.5)
# alpha 设置颜色透明度 0是完全透明 1是完全不透明
plt.fill_between(dates1, highs1, lows1, facecolor='blue', alpha=0.1)

ax.plot(dates2, highs2, color='red', alpha=0.5)
ax.plot(dates2, lows2, color='red', alpha=0.5)
# alpha 设置颜色透明度 0是完全透明 1是完全不透明
plt.fill_between(dates2, highs2, lows2, facecolor='red', alpha=0.1)

ax.set_title('sitka and death_valley, 2021', fontsize=24)
ax.set_xlabel('', fontsize=16)
ax.set_ylabel('Temperature (F)', fontsize=16)
ax.set_ylim(bottom=-10, top=150)

plt.show()
