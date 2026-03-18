import pandas as pd
import requests
import time
import os

# ================= 配置区 =================
INPUT_FILE = "CulRelPro_China_1961-2019.xls"  
OUTPUT_FILE = "CulRelPro_China.xlsx"
AMAP_KEY = "d86996ae9ba1664c74b19fbd29e6d79e" 
# ==========================================

def get_lng_lat(address, name):
    """
    使用高德地图地理编码API获取经纬度
    :param address: 地址
    :param name: 名称（备用）
    :return: 经度, 纬度
    """
    if not address or pd.isna(address):
        address = name
    
    url = "https://restapi.amap.com/v3/geocode/geo"
    params = {
        "key": AMAP_KEY,
        "address": address,
        "output": "json"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        result = response.json()
        
        if result.get("status") == "1" and result.get("geocodes"):
            location = result["geocodes"][0]["location"]
            lng, lat = location.split(",")
            return float(lng), float(lat)
        else:
            print(f"❌ 未找到坐标：{address} -> {result.get('info', '未知错误')}")
            return None, None
    except Exception as e:
        print(f"⚠️ 请求异常：{str(e)}")
        return None, None

def main():
    print(f"📂 正在读取文件：{INPUT_FILE}")
    
    # 1. 读取Excel文件
    if not os.path.exists(INPUT_FILE):
        print(f"❌ 错误：文件 {INPUT_FILE} 不存在")
        return
    
    df = pd.read_excel(INPUT_FILE)
    print(f"✅ 读取到 {len(df)} 条数据")
    
    # 2. 检查必要的列
    required_columns = ["单位名称（中文）", "地址（中文）"]
    if not all(col in df.columns for col in required_columns):
        print(f"❌ 错误：Excel文件必须包含列：{required_columns}")
        print(f"当前列：{list(df.columns)}")
        return
    
    # 3. 获取经纬度
    print("\n📍 开始获取经纬度...")
    lat_list = []
    lng_list = []
    
    for index, row in df.iterrows():
        name = row["单位名称（中文）"]
        address = row["地址（中文）"]
        
        print(f"🔍 正在处理 {index+1}/{len(df)}：{name}")
        
        lng, lat = get_lng_lat(address, name)
        lat_list.append(lat)
        lng_list.append(lng)
        
        # 高德API有频率限制，每请求10次暂停0.5秒
        if (index + 1) % 10 == 0:
            time.sleep(0.5)
    
    # 4. 添加经纬度列
    df["纬度"] = lat_list
    df["经度"] = lng_list
    
    # 5. 保存结果
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"\n🎉 处理完成！结果已保存至：{OUTPUT_FILE}")
    print(f"✅ 成功获取坐标：{df[['纬度', '经度']].notna().sum().sum()} 条")

if __name__ == "__main__":
    main()