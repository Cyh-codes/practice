from pathlib import Path
import matplotlib.pyplot as plt
import csv 
from datetime import datetime

path = Path('CSV解析/weather_data/sitka_weather_2021_full.csv')
lines = path.read_text().splitlines()

reader = csv.reader(lines)
header_row = next(reader)
print(header_row)

dates, prcps = [], []
for row in reader:
    date = datetime.strptime(row[2], '%Y-%m-%d')
    try:
        prcp = float(row[5])
    except ValueError:
        print(f"ValueError: invalid literal for int() with base 10: '0.01' {date}")
    dates.append(date)
    prcps.append(prcp)

plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots()
ax.plot(dates, prcps, color='blue')
title = 'daily prcp, 2021\nSitka_full'
ax.set_title(title, fontsize=20)
ax.set_xlabel('', fontsize=16)
ax.set_ylabel('PRCP ', fontsize=16)

plt.show()