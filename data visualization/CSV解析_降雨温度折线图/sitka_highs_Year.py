from pathlib import Path
import csv 
import matplotlib.pyplot as plt
from datetime import datetime

path = Path('weather_data/sitka_weather_2021_simple.csv')
lines = path.read_text().splitlines()

reader = csv.reader(lines)
header_row = next(reader)

dates, highs = [], []
for row in reader:
    current_date = datetime.strptime(row[2], '%Y-%m-%d')
    high = int(row[4])
    dates.append(current_date)
    highs.append(high)

plt.style.use('seaborn-v0_8')
fig, ax=plt.subplots()
ax.plot(dates, highs, color='red')

ax.set_title('High and Year')
ax.set_xlabel('', fontsize=14)
fig.autofmt_xdate()
ax.set_ylabel('(F)', fontsize=14)
ax.tick_params(labelsize=14)

plt.show()