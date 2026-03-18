import pandas as pd
import json

# 读取Excel文件
df = pd.read_excel('Villages_8.xlsx')

# 删除经纬度为空的行
df_clean = df.dropna(subset=['经度', '纬度'])

# 转换数据格式
data = []
for idx, row in df_clean.iterrows():
    # 当Name_1为NaN时，使用VillageCN作为name
    name = str(row['Name_1']) if pd.notna(row['Name_1']) else str(row['VillageCN'])
    point = {
        'name': name,
        'lng': float(row['经度']),
        'lat': float(row['纬度']),
        'province': str(row['ProvinceCN']),
        'city': str(row['CItyCN']),
        'district': str(row['DistrictCN']),
        'town': str(row['TownCN']),
        'village': str(row['VillageCN'])
    }
    data.append(point)

# 保存为JSON文件
with open('village_points.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'成功转换{len(data)}个村庄点位数据到village_points.json')