from pathlib import Path
import matplotlib.pyplot as plt
import csv 
from datetime import datetime

path = Path('CSV解析/weather_data/death_valley_2021_full.csv')
lines = path.read_text().splitlines()

reader = csv.reader(lines)
header_row = next(reader)
print(header_row)

dates, prcps = [], []
for row in reader:
    date = datetime.strptime(row[2], '%Y-%m-%d')
    try:
        prcp = float(row[3])
    except ValueError:
        # 只要这天没下雨（数据为空），float() 就会报错，程序跳到这里
        print(f"缺失降水数据，已安全跳过该日: {date}")
        
    else:
        # 【关键】只有当 try 里面的 float() 转换成功时，才会执行这部分！
        # 如果报错了，程序执行完 except 就会直接进入下一天的循环，绝对不会装载错误数据。
        dates.append(date)
        prcps.append(prcp)

plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots()
ax.plot(dates, prcps, color='blue')
title = 'daily prcp, 2021\nDeath_valley_full'
ax.set_title(title, fontsize=20)
ax.set_xlabel('', fontsize=16)
ax.set_ylabel('PRCP ', fontsize=16)

plt.show()