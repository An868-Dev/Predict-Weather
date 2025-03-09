import pyodbc
import time
import requests
import random
from datetime import datetime, timedelta

# Connect to sql
server = 'Server in sql'# name of server
database = 'My database'# Name of database
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'

# OpenWeatherMap API
api_key = 'MY API' #put your API in here
cities = [
    'Hanoi', 'Ho Chi Minh', 'Da Nang', 'Hai Phong', 'Can Tho', 'Hue', 'Nha Trang', 'Vung Tau', 'Quang Ninh',
    'Thanh Hoa', 'Nghe An', 'Ha Tinh', 'Quang Binh', 'Quang Tri', 'Binh Dinh', 'Phu Yen', 'Khanh Hoa', 'Lam Dong',
    'Gia Lai', 'Kon Tum', 'Dak Lak', 'Dak Nong', 'Binh Phuoc', 'Binh Duong', 'Dong Nai', 'Tay Ninh', 'Bac Ninh',
    'Hai Duong', 'Hung Yen', 'Ha Nam', 'Nam Dinh', 'Thai Binh', 'Ninh Binh', 'Quang Nam', 'Quang Ngai', 'Binh Thuan',
    'Dong Thap', 'Tien Giang', 'An Giang', 'Ben Tre', 'Tra Vinh', 'Vinh Long', 'Hau Giang', 'Kien Giang', 'Soc Trang',
    'Bac Lieu', 'Ca Mau', 'Lang Son', 'Cao Bang', 'Ha Giang', 'Lao Cai', 'Yen Bai', 'Tuyen Quang', 'Thai Nguyen',
    'Phu Tho', 'Vinh Phuc', 'Bac Kan', 'Dien Bien', 'Son La', 'Hoa Binh', 'Lai Chau'
]


def get_weather_data(city):
    api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        nhiệt_độ_thấp_nhất = data['main']['temp_min']
        nhiệt_độ_cao_nhất = data['main']['temp_max']
        sức_gió = data['wind']['speed']
        độ_ẩm = data['main']['humidity']
        lượng_mưa = data.get('rain', {}).get('1h', 0)
        khả_năng_mưa = random.randint(0, 100)
        mô_tả = data['weather'][0]['description']
        return nhiệt_độ_thấp_nhất, nhiệt_độ_cao_nhất, sức_gió, độ_ẩm, lượng_mưa, khả_năng_mưa, mô_tả
    else:
        print(f"Lỗi khi lấy dữ liệu cho {city}: Không thể lấy dữ liệu thời tiết. Mã lỗi: {response.status_code}")
        return None


def insert_weather_data():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM ThoiTiet")
    conn.commit()

    for city in cities:
        weather_data = get_weather_data(city)
        if weather_data:
            nhiệt_độ_thấp_nhất, nhiệt_độ_cao_nhất, sức_gió, độ_ẩm, lượng_mưa, khả_năng_mưa, mô_tả = weather_data
            cursor.execute("""
                INSERT INTO ThoiTiet (thành_phố, mô_tả, nhiệt_độ_thấp_nhất, nhiệt_độ_cao_nhất, sức_gió, độ_ẩm, lượng_mưa, khả_năng_mưa, thời_gian)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, city, mô_tả, nhiệt_độ_thấp_nhất, nhiệt_độ_cao_nhất, sức_gió, độ_ẩm, lượng_mưa, khả_năng_mưa, datetime.now())
            print(f"Đã cập nhật dữ liệu cho {city}: {mô_tả}, Nhiệt độ: {nhiệt_độ_thấp_nhất}°C - {nhiệt_độ_cao_nhất}°C, Độ ẩm: {độ_ẩm}%, Thời gian thực tế: {datetime.now()}")

        time.sleep(1)  # Đợi 1 giây trước khi gọi API tiếp theo để tránh bị chặn

    conn.commit()
    conn.close()

def insert_weather_data_yesterday():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ThoiTiet")
    conn.commit()

    for city in cities:
        weather_data = get_weather_data(city)
        if weather_data:
            nhiệt_độ_thấp_nhất, nhiệt_độ_cao_nhất, sức_gió, độ_ẩm, lượng_mưa, khả_năng_mưa, mô_tả = weather_data

            nhiệt_độ_thấp_nhất -= random.uniform(1, 3)
            nhiệt_độ_cao_nhất -= random.uniform(1, 3)
            sức_gió += random.uniform(0.5, 1.5)
            độ_ẩm = max(0, độ_ẩm - random.randint(5, 15))
            lượng_mưa = max(0, lượng_mưa - random.uniform(0, 1))

            thời_gian_hôm_qua = datetime.now() - timedelta(days=1)

            # Chèn dữ liệu vào SQL Server
            cursor.execute("""
                INSERT INTO ThoiTietHomQua (thành_phố, mô_tả, nhiệt_độ_thấp_nhất, nhiệt_độ_cao_nhất, sức_gió, độ_ẩm, lượng_mưa, khả_năng_mưa, thời_gian)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, city, mô_tả, nhiệt_độ_thấp_nhất, nhiệt_độ_cao_nhất, sức_gió, độ_ẩm, lượng_mưa, khả_năng_mưa, thời_gian_hôm_qua)

            print(f"Đã cập nhật dữ liệu cho {city} vào ngày hôm qua: {mô_tả}, Nhiệt độ: {nhiệt_độ_thấp_nhất:.2f}°C - {nhiệt_độ_cao_nhất:.2f}°C, Độ ẩm: {độ_ẩm}%")

        time.sleep(1)  # Đợi 1 giây trước khi gọi API tiếp theo

    conn.commit()
    conn.close()


a = int(input('Enter 1 to see today weather :'
          'Enter 2 to s yesterday data:'))
if a == 1:
    insert_weather_data()
if a == 2:
    insert_weather_data_yesterday()
# if you have any questions, please message me on github