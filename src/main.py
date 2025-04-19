import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.watering_page import WateringPage
from pages.settings_page import SettingsPage
from utils.translations import Translations
from utils.weather_api import WeatherAPI

class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.icon_path = "weather.ico"
        self.setWindowIcon(QIcon(self.icon_path))
        
        # Khởi tạo bản dịch trước
        self.translations = Translations()
        self.current_language = "vi"
        
        # Khởi tạo cơ sở dữ liệu người dùng
        self.users_db = {
            "user1": {"password": "1111", "email": "user1@example.com"},
            "user2": {"password": "2222", "email": "user2@example.com"},
            "user3": {"password": "3333", "email": "user3@example.com"},
            "user4": {"password": "4444", "email": "user4@example.com"},
            "user5": {"password": "5555", "email": "user5@example.com"},
        }
        
        # Khởi tạo các biến trạng thái
        self.timer = None
        self.current_user = None
        self.auto_watering_on = False
        self.auto_watering_settings = None
        self.manual_watering_on = False
        self.auto_watering_timer = None
        self.remaining_time = 0
        
        # Khởi tạo API thời tiết với API key
        self.weather_api = WeatherAPI(api_key="4b491ab9f64944de56b3167c89d73ad0")
        
        # Khởi tạo các trang sau khi đã có translations
        self.login_page = LoginPage(self)
        self.main_page = MainPage(self)
        self.watering_page = WateringPage(self)
        self.settings_page = SettingsPage(self)
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.get_translated_text('app_title'))
        self.setMinimumSize(600, 800)
        self.current_page = None
        self.showLoginPage()

    def showLoginPage(self):
        if self.current_page:
            self.current_page.deleteLater()
        self.login_page.show()
        self.current_page = self.login_page

    def showMainPage(self, username):
        try:
            if self.current_page:
                # Kiểm tra xem widget có tồn tại không
                if not self.current_page.isHidden():
                    self.current_page.hide()
                    self.current_page.deleteLater()
                    self.current_page = None
            self.main_page = MainPage(self)  # Khởi tạo lại main_page
            self.main_page.show(username)
            self.current_page = self.main_page
        except Exception as e:
            print(f"Error in showMainPage: {str(e)}")
            # Nếu có lỗi, khởi tạo lại main_page
            self.main_page = MainPage(self)
            self.main_page.show(username)
            self.current_page = self.main_page

    def showWateringOptions(self):
        try:
            if self.current_page:
                # Kiểm tra xem widget có tồn tại không
                if not self.current_page.isHidden():
                    self.current_page.hide()
                    self.current_page.deleteLater()
                    self.current_page = None
            
            # Sử dụng lại watering_page đã có
            self.watering_page.setParent(self)
            self.setCentralWidget(self.watering_page)
            self.watering_page.show()
            self.current_page = self.watering_page
        except Exception as e:
            print(f"Error in showWateringOptions: {str(e)}")
            # Nếu có lỗi, khởi tạo lại watering_page
            self.watering_page = WateringPage(self)
            self.setCentralWidget(self.watering_page)
            self.watering_page.show()
            self.current_page = self.watering_page

    def showSettingsPage(self, username):
        if self.current_page:
            self.current_page.deleteLater()
        self.settings_page.show(username)
        self.current_page = self.settings_page

    def get_translated_text(self, key):
        return self.translations.get_text(key, self.current_language)

    def logout(self):
        if self.timer:
            self.timer.stop()
            self.timer.deleteLater()
            self.timer = None
        self.current_user = None
        self.showLoginPage()

    def updateUI(self):
        # Cập nhật tiêu đề cửa sổ
        self.setWindowTitle(self.get_translated_text('app_title'))
        
        # Cập nhật các trang
        if self.current_page:
            if isinstance(self.current_page, LoginPage):
                self.showLoginPage()
            elif isinstance(self.current_page, MainPage):
                self.showMainPage(self.current_user)
            elif isinstance(self.current_page, WateringPage):
                self.showWateringOptions()
            elif isinstance(self.current_page, SettingsPage):
                self.showSettingsPage(self.current_user)

    def showWeatherDetails(self):
        # Tạo và hiển thị dialog chờ
        please_wait = QMessageBox()
        please_wait.setWindowTitle(self.get_translated_text('loading'))
        please_wait.setText(self.get_translated_text('updating_weather'))
        please_wait.setStandardButtons(QMessageBox.NoButton)
        please_wait.show()
        
        # Cập nhật giao diện
        QApplication.processEvents()
        
        try:
            # Tọa độ của Hồ Chí Minh
            lat = 10.8231
            lon = 106.6297
            
            weather_data = self.weather_api.get_weather_data(lat, lon, self.current_language)
            if weather_data:
                self.main_page.updateWeatherUI(weather_data)
            else:
                QMessageBox.warning(self, self.get_translated_text('error'), 
                    self.get_translated_text('weather_error'))
        except Exception as e:
            QMessageBox.critical(self, self.get_translated_text('error'), 
                f"{self.get_translated_text('error_occurred')}: {str(e)}")
        finally:
            please_wait.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet("""
        QWidget {
            font-family: Arial;
        }
        QLineEdit {
            padding: 8px;
            border-radius: 5px;
            border: 1px solid #ccc;
            margin: 5px 0;
        }
    """)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_()) 