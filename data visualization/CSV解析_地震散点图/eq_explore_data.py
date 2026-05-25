from pathlib import Path
import json

# 将数据作为字符串读取并转换为Python对象
path = Path('eq_data/eq_data_1_day_m1.geojson')  # 指定GeoJSON文件路径
contents = path.read_text()  # 读取文件内容为字符串
all_eq_data = json.loads(contents)  # 解析JSON字符串为Python字典

# 查看数据集中的所有地震
all_eq_dicts = all_eq_data['features']  # 提取所有地震特征列表
print(len(all_eq_dicts))  # 打印地震总数

# 提取地震信息
mags, titles, lons, lats = [],[],[],[]  # 初始化列表存储震级、标题、经度、纬度
for eq_dict in all_eq_dicts:  # 遍历每个地震字典
    # 从属性中提取震级
    mag = eq_dict['properties']['mag']
    # 从属性中提取标题
    title = eq_dict['properties']['title']
    # 从几何坐标中提取经度（坐标数组第一个元素）
    lon = eq_dict['geometry']['coordinates'][0]
    # 从几何坐标中提取纬度（坐标数组第二个元素）
    lat = eq_dict['geometry']['coordinates'][1]
    # 将提取的数据添加到对应列表
    mags.append(mag)
    titles.append(title)
    lons.append(lon)
    lats.append(lat)
# 打印前10个震级
print(mags[:10])
# 打印前2个标题
print(titles[:2])
# 打印前5个经度
print(lons[:5])
# 打印前5个纬度
print(lats[:5])