import pandas as pd
import json

# 读取Excel文件
df = pd.read_excel('all_villages.xlsx')

# 清理数据：移除经纬度为空的行
df_clean = df.dropna(subset=['经度(lng)', '纬度(lat)'])

# 转换数据格式
data = []
for idx, row in df_clean.iterrows():
    point = {
        'name': str(row['VillageCN']) if pd.notna(row['VillageCN']) else str(row['完整地址']),
        'lng': float(row['经度(lng)']),
        'lat': float(row['纬度(lat)']),
        'province': str(row['ProvinceCN']),
        'city': str(row['CItyCN']),
        'district': str(row['DistrictCN']),
        'town': str(row['TownCN']),
        'address': str(row['完整地址'])
    }
    data.append(point)

# 保存为JSON文件
with open('all_villages.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'成功转换 {len(data)} 个传统村落数据到 all_villages.json')
print(f'数据范围: 经度 {min(p["lng"]):.6f} ~ {max(p["lng"]):.6f}, 纬度 {min(p["lat"]):.6f} ~ {max(p["lat"]):.6f}')
