import requests

class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather_data(self, lat, lon, lang="vi"):
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric",  # Lấy nhiệt độ theo độ Celsius
            "lang": lang  # Lấy thông tin thời tiết bằng tiếng Việt
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            print(f"API Response Status: {response.status_code}")  # Debug
            print(f"API Response: {response.text}")  # Debug
            print(f"Request URL: {response.url}")  # Debug URL
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                print("""Lỗi API key:
1. API key chưa được kích hoạt
2. API key không hợp lệ
3. API key không có quyền truy cập""")
                return None
            else:
                print(f"Lỗi API: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Lỗi kết nối: {str(e)}")
            return None
        except Exception as e:
            print(f"Lỗi không xác định: {str(e)}")
            return None 