import pandas as pd
import json

# 读取Excel文件
df = pd.read_excel('CulRelPro_China.xlsx')

# 删除经纬度为空的行
df_clean = df.dropna(subset=['经度', '纬度'])

# 转换数据格式
data = []
for idx, row in df_clean.iterrows():
    point = {
        'name': str(row['单位名称（中文）']),
        'lng': float(row['经度']),
        'lat': float(row['纬度']),
        'address': str(row['地址（中文）']),
        'province': str(row['省级政区名称（中文）']),
        'city': str(row['市级政区名称（中文）']),
        'type': str(row['类型（中文）']),
        'era': str(row['时代（中文）'])
    }
    data.append(point)

# 保存为JSON文件
with open('map_points.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'成功转换{len(data)}个点位数据到map_points.json')