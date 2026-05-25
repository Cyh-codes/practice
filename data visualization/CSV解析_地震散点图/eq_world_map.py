import plotly.express as px
from pathlib import Path
import json

# 读取GeoJSON地震数据文件
path = Path('eq_data/eq_data_1_day_m1.geojson')
# 将文件内容读取为字符串
contents = path.read_text()
# 解析JSON数据为Python字典
all_eq_data = json.loads(contents)

# 提取GeoJSON中的地震特征列表
all_eq_dicts = all_eq_data['features']

# 初始化列表，用于存储震级、标题、经度和纬度
mags, titles, lons, lats = [], [], [], []
# 遍历每个地震特征字典
for eq_dict in all_eq_dicts:
    # 从properties中提取震级
    mag = eq_dict['properties']['mag']
    # 从properties中提取标题
    title = eq_dict['properties']['title']
    # 从geometry的coordinates中提取经度（第一个值）
    lon = eq_dict['geometry']['coordinates'][0]
    # 从geometry的coordinates中提取纬度（第二个值）
    lat = eq_dict['geometry']['coordinates'][1]
    # 将提取的数据添加到对应列表
    mags.append(mag)
    titles.append(title)
    lons.append(lon)
    lats.append(lat)

# 使用Plotly创建散点图，绘制地震位置
fig = px.scatter(
    x=lons,           # x轴为经度
    y=lats,           # y轴为纬度
    labels={'x': '经度', 'y': '纬度'},  # 设置坐标轴标签为中文
    range_x=[-200, 200],  # 设置x轴范围
    range_y=[-90, 90],    # 设置y轴范围
    width=800,            # 图表宽度
    height=800,           # 图表高度
    title='全球地震散点图'  # 图表标题
)
# 将图表保存为HTML文件
fig.write_html('global_earthquakes.html')
# 在浏览器中显示图表
fig.show()