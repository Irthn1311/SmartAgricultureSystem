import serial
import time
import sys
from datetime import datetime
import psycopg2
from psycopg2 import Error

# Cấu hình kết nối database
DB_CONFIG = {
    'dbname': 'smart_agriculture',
    'user': 'postgres',
    'password': '12345678',
    'host': 'localhost',
    'port': '5432'
}

class SensorReader:
    def __init__(self, port='COM3', baud_rate=115200):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = None
        self.db_conn = None
        self.db_cur = None

    def connect_database(self):
        """Kết nối với database và giữ kết nối"""
        try:
            self.db_conn = psycopg2.connect(**DB_CONFIG)
            self.db_cur = self.db_conn.cursor()
            print("Đã kết nối với database thành công")
        except (Exception, Error) as e:
            print(f"Lỗi kết nối database: {e}")
            raise

    def write_to_database(self, data):
        """Ghi dữ liệu cảm biến vào database"""
        try:
            # Thêm dữ liệu vào bảng sensor_data (đầy đủ các cột)
            self.db_cur.execute("""
                INSERT INTO sensor_data (temp, hum, lux, led_status, timestamp)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                float(data['TEMP']),
                float(data['HUM']),
                float(data['LUX']),
                data['LED'],
                data['timestamp']
            ))

            # Commit transaction
            self.db_conn.commit()
            print("Đã ghi dữ liệu vào database")

        except (Exception, Error) as e:
            print(f"Lỗi ghi database: {e}")
            self.db_conn.rollback()

    def parse_sensor_data(self, line):
        """Phân tích dữ liệu cảm biến từ chuỗi serial"""
        data = {}
        try:
            parts = line.split(';')
            for part in parts:
                if ':' in part:
                    key, value = part.split(':')
                    data[key] = value
            return data
        except Exception as e:
            print(f"Lỗi phân tích dữ liệu: {e}")
            return None

    def connect_serial(self):
        """Kết nối với cổng serial"""
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baud_rate,
                timeout=1
            )
            print(f"Đã kết nối với {self.port} ở tốc độ {self.baud_rate} baud")
        except serial.SerialException as e:
            print(f"Lỗi kết nối serial: {e}")
            print(f"Chi tiết lỗi: {str(e)}")
            print(f"Kiểm tra các vấn đề sau:")
            print(f"1. Cổng {self.port} có tồn tại không?")
            print(f"2. Cổng {self.port} đã được kết nối với ESP32 chưa?")
            print(f"3. Cổng {self.port} có đang được sử dụng bởi chương trình khác không?")
            raise

    def wait_for_initialization(self):
        """Chờ các thông báo khởi tạo từ ESP32"""
        while True:
            line = self.ser.readline().decode('utf-8').strip()
            if line:
                print(f"Khởi tạo: {line}")
                if line == "ESPOK":
                    print("ESP32 đã sẵn sàng!")
                    break

    def read_sensor_data(self):
        """Đọc dữ liệu cảm biến từ cổng serial"""
        try:
            # Kết nối serial
            self.connect_serial()
            
            # Kết nối database
            self.connect_database()

            # Chờ khởi tạo
            self.wait_for_initialization()

            # Vòng lặp chính để đọc dữ liệu cảm biến
            while True:
                if self.ser.in_waiting:
                    line = self.ser.readline().decode('utf-8').strip()
                    if line.startswith("TEMP:"):
                        data = self.parse_sensor_data(line)
                        if data:
                            # Thêm thời gian (kiểu datetime)
                            data['timestamp'] = datetime.now()
                            # In dữ liệu
                            print(f"\nThời gian: {data['timestamp']}")
                            print(f"Nhiệt độ: {data['TEMP']}°C")
                            print(f"Độ ẩm: {data['HUM']}%")
                            print(f"Ánh sáng: {data['LUX']} lux")
                            print(f"LED: {data['LED']}")
                            # Ghi dữ liệu vào database
                            self.write_to_database(data)
                time.sleep(0.1)

        except serial.SerialException as e:
            print(f"Lỗi serial: {e}")
            print(f"Chi tiết lỗi: {str(e)}")
        except KeyboardInterrupt:
            print("\nChương trình đã dừng bởi người dùng")
        finally:
            self.cleanup()

    def cleanup(self):
        """Đóng tất cả kết nối"""
        if self.ser:
            self.ser.close()
            print("Đã đóng kết nối serial")
        if self.db_cur:
            self.db_cur.close()
        if self.db_conn:
            self.db_conn.close()
            print("Đã đóng kết nối database")

if __name__ == "__main__":
    # Lấy cổng từ tham số dòng lệnh nếu được cung cấp
    port = sys.argv[1] if len(sys.argv) > 1 else 'COM3'
    
    # Tạo và chạy đối tượng SensorReader
    reader = SensorReader(port)
    reader.read_sensor_data() 