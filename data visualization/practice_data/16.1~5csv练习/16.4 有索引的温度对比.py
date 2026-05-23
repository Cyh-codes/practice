from pathlib import Path
import matplotlib.pyplot as plt
import csv 
from datetime import datetime
import sys
# 看懂了
# ================= 1. 核心进化：定义通用的数据解析函数 =================
def get_weather_data(filepath):
    """
    传入 CSV 文件路径，自动解析表头并返回：日期、最高温、最低温、气象站名称
    """
    path = Path(filepath)
    # 避坑：加上 encoding='utf-8' 防止部分系统下读取包含特殊字符的名称时报错
    lines = path.read_text(encoding='utf-8').splitlines()
    
    reader = csv.reader(lines)
    header_row = next(reader)
    
    # 自动获取索引（不再写死数字）
    try:
        date_idx = header_row.index('DATE')
        tmax_idx = header_row.index('TMAX')
        tmin_idx = header_row.index('TMIN')
        name_idx = header_row.index('NAME')
    except ValueError:
        print(f"致命错误：文件 {filepath} 缺少必要的表头列！")
        sys.exit()

    dates, highs, lows = [], [], []
    station_name = ""

    for row in reader:
        # 自动提取气象站名称（只在第一次循环时提取，避免重复覆盖）
        if not station_name:
            station_name = row[name_idx].title() # title() 让首字母大写更美观
            
        date = datetime.strptime(row[date_idx], '%Y-%m-%d')
        
        try:
            high = int(row[tmax_idx])
            low = int(row[tmin_idx])
        except ValueError:
            # 使用真实的自定义报错信息，而不是伪造的系统报错
            print(f"缺失温度数据，已跳过 {station_name} 的这一天: {date}")
        else:
            dates.append(date)
            highs.append(high)
            lows.append(low)
            
    return dates, highs, lows, station_name

# ================= 2. 极简调用：一行代码获取一地数据 =================
# 调用函数获取锡特卡的数据
dates1, highs1, lows1, name1 = get_weather_data('CSV解析/weather_data/sitka_weather_2021_full.csv')

# 调用函数获取死亡谷的数据
dates2, highs2, lows2, name2 = get_weather_data('CSV解析/weather_data/death_valley_2021_full.csv')

# ================= 3. 可视化渲染 =================
plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots(figsize=(12, 6))

# 绘制锡特卡 (蓝色)
ax.plot(dates1, highs1, color='blue', alpha=0.5, label=name1)
ax.plot(dates1, lows1, color='blue', alpha=0.5)
ax.fill_between(dates1, highs1, lows1, facecolor='blue', alpha=0.1)

# 绘制死亡谷 (红色)
ax.plot(dates2, highs2, color='red', alpha=0.5, label=name2)
ax.plot(dates2, lows2, color='red', alpha=0.5)
ax.fill_between(dates2, highs2, lows2, facecolor='red', alpha=0.1)

# 【核心要求】动态生成图表标题
# 使用 f-string 将自动获取的两个气象站名称拼接到标题中
title = f"Temperature Comparison, 2021\n{name1} vs {name2}"
ax.set_title(title, fontsize=20, pad=15)

ax.set_xlabel('', fontsize=16)
ax.set_ylabel('Temperature (F)', fontsize=16)
ax.set_ylim(bottom=-10, top=150)

# 优化日期显示并添加图例
fig.autofmt_xdate()
ax.legend(loc='best', fontsize=12)

plt.show()