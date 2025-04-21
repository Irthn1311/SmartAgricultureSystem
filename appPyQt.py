import sys
import os
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import joblib
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QLineEdit, QMessageBox, QFrame, QSizePolicy, 
    QButtonGroup, QGridLayout, QGroupBox, QFormLayout, QSpinBox, 
    QTimeEdit, QComboBox, QScrollArea, QCheckBox, QFileDialog, QDialog
)
from PyQt5.QtCore import Qt, QTimer, QDateTime, QLocale
from PyQt5.QtGui import QIcon, QPixmap, QRegion

class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Khởi tạo database người dùng
        self.users_db = {
            "user1": {"password": "1111", "email": "user1@example.com"},
            "user2": {"password": "2222", "email": "user2@example.com"},
            "user3": {"password": "3333", "email": "user3@example.com"},
            "user4": {"password": "4444", "email": "user4@example.com"},
            "user5": {"password": "5555", "email": "user5@example.com"},
        }
        self.current_user = None  # Biến lưu người dùng hiện tại
        self.timer = None  # Khởi tạo timer
        self.current_language = "vi"  
        self.languages = {
            "vi": "Tiếng Việt",
            "en": "English",
            "auto": "Tự động theo hệ thống"
        }# Mặc định là tiếng Việt
        self.translations = {
            "vi": {
                "app_title": "Hệ thống Nông nghiệp Thông minh",
                "system_title": "Hệ thống quản lý nông nghiệp thông minh",
                "username": "Tên đăng nhập",
                "password": "Mật khẩu",
                "login": "Đăng nhập",
                "show_password": "Hiện mật khẩu",
                "settings": "Cài đặt",
                "logout": "Đăng xuất",
                "weather": "Thời tiết",
                "watering": "Tưới nước",
                "home": "Trang chủ",
                "monday": "Thứ hai",
                "tuesday": "Thứ ba",
                "wednesday": "Thứ tư",
                "thursday": "Thứ năm",
                "friday": "Thứ sáu",
                "saturday": "Thứ bảy",
                "sunday": "Chủ nhật",
                "temperature": "Nhiệt độ",
                "humidity": "Độ ẩm",
                "cloud": "Mây",
                "rain_prob": "Xác suất mưa",
                "loading": "Đang tải",
                "updating_weather": "Đang cập nhật thông tin thời tiết...",
                "weather_error": "Lỗi khi cập nhật thông tin thời tiết",
                "error": "Lỗi",
                "yesterday": "Hôm qua",
                "today": "Hôm nay",
                "next_day": "ngày tiếp theo",
                "sunny": "Nắng",
                "rainy": "Mưa",
                "watering_options": "Tùy chọn tưới nước",
                "manual_watering": "Tưới thủ công",
                "auto_watering": "Tưới tự động",
                "manual_watering_desc": "Điều khiển trực tiếp việc tưới nước",
                "auto_watering_desc": "Tự động tưới theo lịch trình",
                "system_on": "Hệ thống đang BẬT",
                "system_off": "Hệ thống đang TẮT",
                "on": "BẬT",
                "off": "TẮT",
                "back": "Quay lại",
                "auto_watering_title": "Cài đặt tưới tự động",
                "auto_system_on": "Hệ thống tưới tự động đang BẬT",
                "auto_system_off": "Hệ thống tưới tự động đang TẮT",
                "auto_watering_settings": "Cài đặt tưới tự động",
                "start_time_label": "Thời gian bắt đầu:",
                "end_time_label": "Thời gian kết thúc:",
                "cycle_label": "Chu kỳ tưới:",
                "duration_label": "Thời gian mỗi lần tưới:",
                "minutes": "phút",
                "cycle_30min": "30 phút một lần",
                "cycle_1hour": "1 giờ một lần",
                "cycle_2hours": "2 giờ một lần",
                "cycle_4hours": "4 giờ một lần",
                "operating_time": "Thời gian hoạt động:",
                "watering_cycle": "Chu kỳ tưới:",
                "watering_duration": "Thời gian tưới:",
                "back_btn": "Quay lại",
                "activate_btn": "Kích hoạt",
                "deactivate_btn": "Vô hiệu hóa"
            },
            "en": {
                "app_title": "Smart Agriculture System",
                "system_title": "Smart Agriculture Management System",
                "username": "Username",
                "password": "Password",
                "login": "Login",
                "show_password": "Show password",
                "settings": "Settings",
                "logout": "Logout",
                "weather": "Weather",
                "watering": "Watering",
                "home": "Home",
                "monday": "Monday",
                "tuesday": "Tuesday",
                "wednesday": "Wednesday",
                "thursday": "Thursday",
                "friday": "Friday",
                "saturday": "Saturday",
                "sunday": "Sunday",
                "temperature": "Temperature",
                "humidity": "Humidity",
                "cloud": "Cloud",
                "rain_prob": "Rain Probability",
                "loading": "Loading",
                "updating_weather": "Updating weather information...",
                "weather_error": "Error updating weather information",
                "error": "Error",
                "yesterday": "Yesterday",
                "today": "Today",
                "next_day": "day ahead",
                "sunny": "Sunny",
                "rainy": "Rainy",
                "watering_options": "Watering Options",
                "manual_watering": "Manual Watering",
                "auto_watering": "Automatic Watering",
                "manual_watering_desc": "Direct control of watering",
                "auto_watering_desc": "Automatic watering on schedule",
                "system_on": "System is ON",
                "system_off": "System is OFF",
                "on": "ON",
                "off": "OFF",
                "back": "Back",
                "auto_watering_title": "Automatic Watering Settings",
                "auto_system_on": "Automatic Watering System is ON",
                "auto_system_off": "Automatic Watering System is OFF",
                "auto_watering_settings": "Automatic Watering Settings",
                "start_time_label": "Start Time:",
                "end_time_label": "End Time:",
                "cycle_label": "Watering Cycle:",
                "duration_label": "Watering Duration:",
                "minutes": "minutes",
                "cycle_30min": "Every 30 minutes",
                "cycle_1hour": "Every hour",
                "cycle_2hours": "Every 2 hours",
                "cycle_4hours": "Every 4 hours",
                "operating_time": "Operating Time:",
                "watering_cycle": "Watering Cycle:",
                "watering_duration": "Watering Duration:",
                "back_btn": "Back",
                "activate_btn": "Activate",
                "deactivate_btn": "Deactivate"
            }
        }
        # Khởi tạo trạng thái tưới nước
        self.manual_watering_on = False
        self.auto_watering_on = False
        self.auto_watering_settings = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.get_translated_text('app_title'))
    
        # Điều chỉnh kích thước cửa sổ
        self.resize(700, 900)
        self.setMinimumSize(400, 600)
        self.setMaximumSize(800, 1200)

        # Chỉnh kích thước font chữ cho khung giao diện
        self.setStyleSheet("""
            QLabel {
                font-size: 12px;
            }
            QLineEdit {
                font-size: 12px;
            }
            QPushButton {
                font-size: 12px;
            }
            QCheckBox {
                font-size: 12px;
            }
        """)

        self.current_page = None
        self.showLoginPage()

    def showLoginForm(self):
        self.showMainPage()

    def showLoginPage(self):
        if self.current_page:
            self.current_page.deleteLater()

        login_widget = QWidget()
        layout = QVBoxLayout(login_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)

        # Container widget để căn giữa form đăng nhập
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(25)

        # Tiêu đề
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setSpacing(15)

        # Logo hoặc icon
        logo_label = QLabel("🌱")
        logo_label.setStyleSheet("""
            font-size: 60px;
            margin-bottom: 15px;
        """)
        title_layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        # Tên ứng dụng
        app_name = QLabel(self.get_translated_text('system_title'))
        app_name.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #2E7D32;
            margin-bottom: 8px;
        """)
        title_layout.addWidget(app_name, alignment=Qt.AlignCenter)

        # Subtitle
        subtitle = QLabel("Smart Agriculture Management System")
        subtitle.setStyleSheet("""
            font-size: 18px;
            color: #666;
            margin-bottom: 20px;
        """)
        title_layout.addWidget(subtitle, alignment=Qt.AlignCenter)

        container_layout.addWidget(title_container)

        # Form container
        form_container = QWidget()
        form_container.setObjectName("form_container")
        form_container.setStyleSheet("""
            QWidget#form_container {
                background-color: white;
                border-radius: 18px;
                padding: 30px;
                border: 2px solid #4CAF50;
            }
        """)
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(25, 25, 25, 25)
        form_layout.setSpacing(20)

        # Form title
        login_title = QLabel(self.get_translated_text('login'))
        login_title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin: 10px 0px 20px 0px;
        """)
        form_layout.addWidget(login_title, alignment=Qt.AlignCenter)

        # Ô nhập username
        username_container = QWidget()
        username_container.setObjectName("username_container")
        username_container.setStyleSheet("""
            QWidget#username_container {
                background-color: #f9f9f9;
                border-radius: 12px;
                border: 1px solid #ddd;
            }
        """)
        username_layout = QVBoxLayout(username_container)
        username_layout.setSpacing(8)
        username_layout.setContentsMargins(15, 15, 15, 15)
        
        username_label = QLabel(self.get_translated_text('username'))
        username_label.setStyleSheet("""
            font-size: 16px;
            padding: 3px 0px 3px 3px;
            font-weight: bold;
            color: #666;
        """)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText(self.get_translated_text('Hãy nhập tài khoản của bạn...'))
        self.username_input.setStyleSheet("""
            QLineEdit {
                font-size: 15px;
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: white;
            }
        """)
        self.username_input.setMinimumHeight(40)
        self.username_input.textChanged.connect(self.validateInputs)
        
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        form_layout.addWidget(username_container)

        # Ô nhập password
        password_container = QWidget()
        password_container.setObjectName("password_container")
        password_container.setStyleSheet("""
            QWidget#password_container {
                background-color: #f9f9f9;
                border-radius: 12px;
                border: 1px solid #ddd;
            }
        """)
        password_layout = QVBoxLayout(password_container)
        password_layout.setSpacing(8)
        password_layout.setContentsMargins(15, 15, 15, 15)
        
        password_label = QLabel(self.get_translated_text('password'))
        password_label.setStyleSheet("""
            font-size: 16px;
            padding: 3px 0px 3px 3px;
            font-weight: bold;
            color: #666;
        """)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(self.get_translated_text('Hãy nhập mật khẩu của bạn...'))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                font-size: 15px;
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: white;
            }
        """)
        self.password_input.setMinimumHeight(40)
        self.password_input.textChanged.connect(self.validateInputs)
        
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        form_layout.addWidget(password_container)

        # Checkbox hiển thị mật khẩu
        show_password_cb = QCheckBox(self.get_translated_text('show_password'))
        show_password_cb.setStyleSheet("""
            QCheckBox {
                font-size: 15px;
                color: #666;
                padding: 8px;
                margin-left: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)
        show_password_cb.stateChanged.connect(self.togglePasswordVisibility)
        form_layout.addWidget(show_password_cb)

        # Nút đăng nhập
        login_btn = QPushButton(self.get_translated_text('login'))
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 12px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                min-width: 150px;
                margin-top: 15px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        login_btn.clicked.connect(self.handleLogin)
        form_layout.addWidget(login_btn, alignment=Qt.AlignCenter)

        # Label hiển thị thông báo
        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("""
            font-size: 15px;
            padding: 10px;
            margin-top: 12px;
            color: #666;
        """)
        form_layout.addWidget(self.message_label)

        container_layout.addWidget(form_container)
        layout.addWidget(container, alignment=Qt.AlignCenter)

        login_widget.setLayout(layout)
        self.setCentralWidget(login_widget)
        self.current_page = login_widget

    def validateInputs(self):
        # Lấy text từ các input
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        # Tìm các container
        username_container = self.findChild(QWidget, "username_container")
        password_container = self.findChild(QWidget, "password_container")

        # Kiểm tra và cập nhật style cho username container
        if username:
            username_container.setStyleSheet("""
                QWidget#username_container {
                    background-color: #f9f9f9;
                    border-radius: 10px;
                    border: 2px solid #4CAF50;
                }
            """)
        else:
            username_container.setStyleSheet("""
                QWidget#username_container {
                    background-color: #f9f9f9;
                    border-radius: 10px;
                    border: 2px solid #f44336;
                }
            """)

        # Kiểm tra và cập nhật style cho password container
        if password:
            password_container.setStyleSheet("""
                QWidget#password_container {
                    background-color: #f9f9f9;
                    border-radius: 10px;
                    border: 2px solid #4CAF50;
                }
            """)
        else:
            password_container.setStyleSheet("""
                QWidget#password_container {
                    background-color: #f9f9f9;
                    border-radius: 10px;
                    border: 2px solid #f44336;
                }
            """)

    def handleLogin(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        # Gọi validateInputs để cập nhật style trước khi kiểm tra
        self.validateInputs()

        if not username or not password:
            self.message_label.setText(self.get_translated_text('please_fill_all'))
            self.message_label.setStyleSheet("""
                color: #f44336;
                font-size: 18px;
                padding: 15px;
            """)
            return

        if username not in self.users_db or self.users_db[username]["password"] != password:
            self.message_label.setText(self.get_translated_text('invalid_credentials'))
            self.message_label.setStyleSheet("""
                color: #f44336;
                font-size: 18px;
                padding: 15px;
            """)
            # Đặt lại style cho password container khi sai mật khẩu
            password_container = self.findChild(QWidget, "password_container")
            password_container.setStyleSheet("""
                QWidget#password_container {
                    background-color: #f9f9f9;
                    border-radius: 10px;
                    border: 2px solid #f44336;
                }
            """)
            return

        self.current_user = username
        self.message_label.setText(self.get_translated_text('login_success'))
        self.message_label.setStyleSheet("""
            color: #4CAF50;
            font-size: 18px;
            padding: 15px;
        """)
        QTimer.singleShot(1000, lambda: self.showMainPage(username))

    def togglePasswordVisibility(self, state):
        if state == Qt.Checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

    def showMainPage(self, username):
        if self.current_page:
            self.current_page.deleteLater()
            
        # Dừng timer cũ nếu có
        if self.timer:
            self.timer.stop()
            self.timer.deleteLater()

        dashboard = QWidget()
        main_layout = QVBoxLayout(dashboard)

        # Header
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)

        # User Info Widget
        user_info_widget = QWidget()
        user_info_layout = QHBoxLayout(user_info_widget)

        # User Image
        self.user_image_label = QLabel()
        self.user_image_label.setScaledContents(True)
        self.user_image_label.setFixedSize(50, 50)
        self.user_image_label.mousePressEvent = lambda event: self.uploadImage(username)
        if "image" in self.users_db[username]:
            user_image = QPixmap(self.users_db[username]["image"])
            self.user_image_label.setPixmap(user_image)
        else:
            self.user_image_label.setText("Chọn ảnh")
            self.user_image_label.setStyleSheet("border: 1px dashed #ccc; padding: 10px;")

        # Tạo mặt nạ hình tròn
        mask = QRegion(0, 0, 50, 50, QRegion.Ellipse)
        self.user_image_label.setMask(mask)

        user_info_layout.addWidget(self.user_image_label)

        # Username Label
        username_label = QLabel(username)
        username_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        user_info_layout.addWidget(username_label)

        header_layout.addWidget(user_info_widget)

        # Logout Button với thiết kế mới
        logout_btn = QPushButton(self.get_translated_text('logout'))
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 8px 15px;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        logout_btn.clicked.connect(self.confirmLogout)
        header_layout.addWidget(logout_btn, alignment=Qt.AlignRight)

        # Widget thời gian
        time_widget = QWidget()
        time_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        time_layout = QVBoxLayout(time_widget)

        self.time_label = QLabel("00:00")
        self.date_label = QLabel("Ngày, 00-00-0000")

        self.time_label.setAlignment(Qt.AlignCenter)
        self.date_label.setAlignment(Qt.AlignCenter)

        self.time_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #333;")
        self.date_label.setStyleSheet("font-size: 16px; color: #666;")

        time_layout.addWidget(self.time_label)
        time_layout.addWidget(self.date_label)

        time_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
                padding: 10px;
            }
        """)

        # Widget thời tiết
        weather_widget = QWidget()
        weather_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        weather_layout = QVBoxLayout(weather_widget)

        # Icon và trạng thái thời tiết
        status_widget = QWidget()
        status_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        status_layout = QHBoxLayout(status_widget)

        self.weather_icon = QLabel("☀️")
        self.weather_text = QLabel("Nắng")
        
        self.weather_icon.setObjectName("weather_icon")
        self.weather_text.setObjectName("weather_text")

        self.weather_icon.setStyleSheet("font-size: 48px;")
        self.weather_text.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")

        status_layout.addWidget(self.weather_icon, alignment=Qt.AlignCenter)
        status_layout.addWidget(self.weather_text, alignment=Qt.AlignCenter)

        # Thông số thời tiết
        params_widget = QWidget()
        params_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        params_grid = QGridLayout(params_widget)
        params_grid.setSpacing(15)

        self.params = [
            ("🌡", self.get_translated_text('temperature'), "**", "°C"),
            ("💨", self.get_translated_text('wind_speed'), "**", "km/h"),
            ("💧", self.get_translated_text('humidity'), "**", "%"),
            ("🏗", self.get_translated_text('precipitation'), "**", "%")
        ]

        # Tạo line dọc
        vline = QFrame()
        vline.setFrameShape(QFrame.VLine)
        vline.setFrameShadow(QFrame.Sunken)
        vline.setStyleSheet("background-color: #ccc;")

        for i, (icon, label, value, unit) in enumerate(self.params):
            param_widget = QWidget()
            param_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            param_layout = QHBoxLayout(param_widget)

            # Left side (icon + label)
            left = QLabel(f"{icon} {label}")
            left.setStyleSheet("font-size: 14px; color: #333;")

            # Right side (value + unit)
            right = QLabel(f"{value}{unit}")
            right.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")

            param_layout.addWidget(left)
            param_layout.addStretch()
            param_layout.addWidget(right)

            row = i // 2
            col = i % 2

            if col == 1:
                params_grid.addWidget(vline, row, 1)
            params_grid.addWidget(param_widget, row, col * 2 + (1 if col == 1 else 0))

        weather_layout.addWidget(status_widget)
        weather_layout.addWidget(params_widget)

        weather_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
            }
        """)

        # Navigation bar
        nav_bar = QWidget()
        nav_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setSpacing(10)

        nav_buttons = [
            ("🏠", self.get_translated_text('home')),
            ("🌤", self.get_translated_text('weather')),
            ("💧", self.get_translated_text('watering')),
            ("⚙️", self.get_translated_text('settings'))
        ]

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        for icon, tooltip in nav_buttons:
            btn = QPushButton(icon)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setCheckable(True)
            btn.setToolTip(tooltip)
            nav_layout.addWidget(btn)
            self.button_group.addButton(btn)

        nav_bar.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
                padding: 10px;
            }
            QPushButton {
                border: none;
                border-radius: 10px;
                padding: 15px;
                font-size: 20px;
                background-color: #f0f0f0;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:checked {
                background-color: #4a90e2;
                color: white;
            }
        """)

        # Thêm tất cả vào layout chính
        main_layout.addWidget(header_widget)
        main_layout.addWidget(time_widget)
        main_layout.addWidget(weather_widget)
        main_layout.addStretch()
        main_layout.addWidget(nav_bar)

        dashboard.setStyleSheet("background-color: #f5f6fa;")

        # Cập nhật thời gian
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)

        self.setCentralWidget(dashboard)
        self.current_page = dashboard

        # Set trang chủ là active và cập nhật thời gian
        self.button_group.buttons()[0].setChecked(True)
        self.updateDateTime()

        # Kết nối sự kiện click vào các nút
        self.button_group.buttons()[1].clicked.connect(self.showWeatherDetails)
        self.button_group.buttons()[2].clicked.connect(self.showWateringOptions)
        self.button_group.buttons()[3].clicked.connect(lambda: self.showSettingsPage(username))

    def updateDateTime(self):
        try:
            if hasattr(self, 'time_label') and self.time_label and not self.time_label.isHidden():
                current = QDateTime.currentDateTime()
                self.time_label.setText(current.toString("HH:mm"))

                # Chuyển đổi thứ sang ngôn ngữ đã chọn
                weekday_map = {
                    1: 'monday',
                    2: 'tuesday', 
                    3: 'wednesday',
                    4: 'thursday',
                    5: 'friday',
                    6: 'saturday',
                    0: 'sunday'
                }

                weekday = current.date().dayOfWeek() % 7
                weekday_text = self.get_translated_text(weekday_map[weekday])
                
                # Format ngày tháng theo ngôn ngữ
                if self.current_language == "en":
                    date_str = f"{weekday_text}, {current.toString('MM-dd-yyyy')}"
                else:
                    date_str = f"{weekday_text}, {current.toString('dd-MM-yyyy')}"

                if hasattr(self, 'date_label') and self.date_label:
                    self.date_label.setText(date_str)

        except RuntimeError:
            # Nếu widget đã bị xóa, dừng timer
            if self.timer:
                self.timer.stop()
                self.timer.deleteLater()
                self.timer = None

    def uploadImage(self, username):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Chọn ảnh", "", "Image Files (*.png *.jpg *.jpeg)")

        if file_path:
            self.users_db[username]["image"] = file_path
            user_image = QPixmap(file_path)
            self.user_image_label.setPixmap(user_image)

            # Cập nhật mặt nạ hình tròn sau khi tải ảnh mới
            mask = QRegion(0, 0, 50, 50, QRegion.Ellipse)
            self.user_image_label.setMask(mask)

    def showWeatherDetails(self):
        try:
            # Kiểm tra sự tồn tại của các file cần thiết
            required_files = {
                "Weather_Data.csv": "File dữ liệu thời tiết",
                "scaler.save": "File scaler đã train",
                "weather_model.keras": "File model dự đoán thời tiết"
            }
            
            missing_files = []
            for file_path, file_desc in required_files.items():
                if not os.path.exists(file_path):
                    missing_files.append(f"{file_desc} ({file_path})")
            
            if missing_files:
                error_msg = "Không tìm thấy các file sau:\n" + "\n".join(missing_files)
                error_msg += "\n\nVui lòng đảm bảo các file trên tồn tại trong thư mục chương trình."
                QMessageBox.critical(self, self.get_translated_text('error'), error_msg)
                return
            
            # Load và tiền xử lý dữ liệu
            df = pd.read_csv("Weather_Data.csv")
            features = self.preprocess_data(df)
            
            # Load model và scaler
            scaler = joblib.load("scaler.save")
            model = load_model("weather_model.keras")
            
            # Chuẩn hóa dữ liệu
            scaled_features = scaler.transform(features)
            
            # Lấy 3 ngày cuối cùng cho input
            X_input = scaled_features[-3:]
            X_input = X_input.reshape((1, 3, 6))
            
            # Dự đoán
            predictions = model.predict(X_input)[0]
            
            # Cập nhật UI với kết quả dự đoán
            self.updateWeatherUI(predictions, features)
            
        except pd.errors.EmptyDataError:
            QMessageBox.critical(self, self.get_translated_text('error'),
                "File dữ liệu thời tiết trống hoặc không đúng định dạng.")
        except Exception as e:
            QMessageBox.critical(self, self.get_translated_text('error'),
                f"{self.get_translated_text('weather_error')}\n{str(e)}")

    def preprocess_data(self, df):
        # Chuyển đổi RainToday
        df['RainToday'] = df['RainToday'].map({'Yes': 1, 'No': 0})
        
        # Xử lý missing values
        df.dropna(inplace=True)
        
        # Chọn features
        features = ['MinTemp', 'MaxTemp', 'Humidity', 'Cloud', 'Temp', 'RainToday']
        
        return df[features]

    def updateWeatherUI(self, predictions, features):
        try:
            # Tạo widget chính chứa tất cả nội dung
            main_container = QWidget()
            main_layout = QVBoxLayout(main_container)
            main_layout.setSpacing(20)
            
            # Tạo widget chứa thông tin thời tiết
            weather_container = QWidget()
            weather_layout = QVBoxLayout(weather_container)
            weather_layout.setSpacing(20)
            
            # Tạo scroll area để cuộn khi có nhiều widget
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            
            # Widget chứa nội dung có thể cuộn
            scroll_content = QWidget()
            scroll_layout = QVBoxLayout(scroll_content)
            
            # Lấy thông tin thời tiết cho hôm qua và hôm nay từ dataset
            yesterday_data = features.iloc[-2]
            today_data = features.iloc[-1]
            
            # Widget cho hôm qua - chỉ hiển thị trạng thái thời tiết
            yesterday_widget = self.createWeatherWidget(
                self.get_translated_text('yesterday'), 
                self.get_translated_text('sunny') if yesterday_data['RainToday'] == 0 
                else self.get_translated_text('rainy'),
                None,  # Không truyền data để không hiển thị chỉ số
                None,  # Không hiển thị xác suất mưa
                show_details=False  # Không hiển thị chi tiết
            )
            
            # Widget cho hôm nay - hiển thị đầy đủ thông tin
            today_widget = self.createWeatherWidget(
                self.get_translated_text('today'),
                self.get_translated_text('rainy') if today_data['RainToday'] == 1 
                else self.get_translated_text('sunny'),
                today_data,
                None,  # Không hiển thị xác suất mưa cho hôm nay
                show_details=True  # Hiển thị đầy đủ chi tiết
            )
            
            # Thêm widget hôm qua và hôm nay
            scroll_layout.addWidget(yesterday_widget)
            scroll_layout.addWidget(today_widget)
            
            # Thêm dự báo cho 3 ngày tiếp theo - chỉ hiển thị dự đoán và xác suất
            for i, day in enumerate(predictions):
                prob_rain = day[1] * 100
                will_rain = self.get_translated_text('rainy') if np.argmax(day) == 1 else self.get_translated_text('sunny')
                
                future_widget = self.createWeatherWidget(
                    f"{i+1} {self.get_translated_text('next_day')}",
                    will_rain,
                    None,  # Không truyền data vì không hiển thị chỉ số
                    prob_rain,  # Chỉ hiển thị xác suất mưa
                    show_details=False  # Không hiển thị chi tiết
                )
                scroll_layout.addWidget(future_widget)
            
            # Thêm spacing ở cuối
            scroll_layout.addStretch()
            
            # Set widget cho scroll area
            scroll.setWidget(scroll_content)
            weather_layout.addWidget(scroll)
            
            # Thêm weather container vào main layout
            main_layout.addWidget(weather_container)
            
            # Thêm thanh điều hướng
            nav_bar = QWidget()
            nav_layout = QHBoxLayout(nav_bar)
            nav_layout.setSpacing(10)
            
            nav_buttons = [
                ("🏠", self.get_translated_text('home')),
                ("🌤", self.get_translated_text('weather')),
                ("💧", self.get_translated_text('watering')),
                ("⚙️", self.get_translated_text('settings'))
            ]
            
            self.button_group = QButtonGroup(self)
            self.button_group.setExclusive(True)
            
            for icon, tooltip in nav_buttons:
                btn = QPushButton(icon)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                btn.setCheckable(True)
                btn.setToolTip(tooltip)
                nav_layout.addWidget(btn)
                self.button_group.addButton(btn)
            
            # Set style cho thanh điều hướng
            nav_bar.setStyleSheet("""
                QWidget {
                    background-color: white;
                    border-radius: 15px;
                    padding: 10px;
                }
                QPushButton {
                    border: none;
                    border-radius: 10px;
                    padding: 15px;
                    font-size: 20px;
                    background-color: #f0f0f0;
                    min-width: 60px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QPushButton:checked {
                    background-color: #4a90e2;
                    color: white;
                }
            """)
            
            # Kết nối sự kiện cho các nút
            self.button_group.buttons()[0].clicked.connect(lambda: self.showMainPage(self.current_user))
            self.button_group.buttons()[1].clicked.connect(self.showWeatherDetails)
            self.button_group.buttons()[2].clicked.connect(self.showWateringOptions)
            self.button_group.buttons()[3].clicked.connect(lambda: self.showSettingsPage(self.current_user))
            
            # Set nút thời tiết là active
            self.button_group.buttons()[1].setChecked(True)
            
            # Thêm thanh điều hướng vào main layout
            main_layout.addWidget(nav_bar)
            
            # Xóa widget cũ nếu có
            if self.current_page:
                self.current_page.deleteLater()
            
            # Đặt widget mới làm central widget
            self.setCentralWidget(main_container)
            self.current_page = main_container

        except Exception as e:
            print(f"Lỗi khi cập nhật giao diện: {str(e)}")
            raise Exception(f"Không thể cập nhật giao diện thời tiết: {str(e)}")

    def createWeatherWidget(self, title, weather_status, data=None, rain_prob=None, show_details=True):
        widget = QWidget()
        widget.setObjectName("weather_widget")
        layout = QVBoxLayout(widget)
        
        # Tiêu đề
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)
        
        # Icon và trạng thái thời tiết
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        
        weather_icon = "🌧️" if self.get_translated_text('rainy') in weather_status else "☀️"
        icon_label = QLabel(weather_icon)
        icon_label.setStyleSheet("font-size: 48px;")
        status_layout.addWidget(icon_label)
        
        status_label = QLabel(weather_status)
        status_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        status_layout.addWidget(status_label)
        
        layout.addWidget(status_widget)
        
        # Thông số thời tiết - chỉ hiển thị nếu show_details=True và có data
        if show_details and data is not None:
            params_widget = QWidget()
            params_layout = QGridLayout(params_widget)
            
            # Định nghĩa các thông số cần hiển thị
            params = [
                ("🌡️", self.get_translated_text('temperature'), f"{data.get('Temp', 0):.1f}°C"),
                ("💧", self.get_translated_text('humidity'), f"{data.get('Humidity', 0):.1f}%"),
                ("☁️", self.get_translated_text('cloud'), f"{data.get('Cloud', 0):.1f}%")
            ]
            
            # Thêm các thông số vào grid
            for i, (icon, label, value) in enumerate(params):
                icon_label = QLabel(icon)
                icon_label.setStyleSheet("font-size: 20px;")
                params_layout.addWidget(icon_label, i, 0)
                
                param_label = QLabel(label)
                param_label.setStyleSheet("font-size: 14px; color: #666;")
                params_layout.addWidget(param_label, i, 1)
                
                value_label = QLabel(value)
                value_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
                params_layout.addWidget(value_label, i, 2)
            
            layout.addWidget(params_widget)
        
        # Thêm xác suất mưa nếu có
        if rain_prob is not None:
            rain_prob_widget = QWidget()
            rain_prob_layout = QHBoxLayout(rain_prob_widget)
            
            rain_prob_label = QLabel(f"🌧️ {self.get_translated_text('rain_prob')}")
            rain_prob_label.setStyleSheet("font-size: 14px; color: #666;")
            rain_prob_layout.addWidget(rain_prob_label)
            
            rain_prob_value = QLabel(f"{rain_prob:.1f}%")
            rain_prob_value.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
            rain_prob_layout.addWidget(rain_prob_value)
            
            layout.addWidget(rain_prob_widget)
        
        # Style cho widget
        widget.setStyleSheet("""
            QWidget#weather_widget {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
                margin: 10px;
            }
        """)
        
        return widget

    def confirmLogout(self):
        self.logout()  # Gọi trực tiếp hàm logout mà không hiển thị thông báo

    def showWateringOptions(self):
        if self.current_page:
            self.current_page.deleteLater()

        watering_widget = QWidget()
        main_layout = QVBoxLayout(watering_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Tiêu đề
        title = QLabel(self.get_translated_text('watering_options'))
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            margin: 20px 0;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 10px;
            text-align: center;
        """)
        content_layout.addWidget(title, alignment=Qt.AlignCenter)

        # Container cho các nút chọn chế độ
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setSpacing(30)

        # Nút chọn chế độ tưới thủ công
        manual_btn = QPushButton()
        manual_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 3px solid rgba(92, 83, 78, 0.07);
                border-radius: 15px;
                padding: 5px;
                min-width: 150px;
                min-height: 150px;
            }
            QPushButton:hover {
                background-color: #FF6B6B;
            }
            QPushButton:hover QLabel {
                color: white;
            }
        """)
        manual_layout = QVBoxLayout(manual_btn)
        
        manual_icon = QLabel("🚰")
        manual_icon.setStyleSheet("font-size: 40px;")
        manual_text = QLabel(self.get_translated_text('manual_watering'))
        manual_text.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color:rgb(0, 47, 255);
        """)
        manual_desc = QLabel(self.get_translated_text('manual_watering_desc'))
        manual_desc.setStyleSheet("""
            font-size: 16px;
            color: #666;
        """)
        manual_desc.setAlignment(Qt.AlignCenter)
        
        manual_layout.addWidget(manual_icon, alignment=Qt.AlignCenter)
        manual_layout.addWidget(manual_text, alignment=Qt.AlignCenter)
        manual_layout.addWidget(manual_desc, alignment=Qt.AlignCenter)

        # Nút chọn chế độ tưới tự động
        auto_btn = QPushButton()
        auto_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 3px solid rgba(92, 83, 78, 0.07);
                border-radius: 7px;
                padding: 5px;
                min-width: 150px;
                min-height: 150px;
            }
            QPushButton:hover {
                background-color: #FF6B6B;
            }
            QPushButton:hover QLabel {
                color: white;
            }
        """)
        auto_layout = QVBoxLayout(auto_btn)
        
        auto_icon = QLabel("🤖")
        auto_icon.setStyleSheet("font-size:40px;")
        auto_text = QLabel(self.get_translated_text('auto_watering'))
        auto_text.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color:rgb(81, 255, 0);
        """)
        auto_desc = QLabel(self.get_translated_text('auto_watering_desc'))
        auto_desc.setStyleSheet("""
            font-size: 16px;
            color: #666;
        """)
        auto_desc.setAlignment(Qt.AlignCenter)
        
        auto_layout.addWidget(auto_icon, alignment=Qt.AlignCenter)
        auto_layout.addWidget(auto_text, alignment=Qt.AlignCenter)
        auto_layout.addWidget(auto_desc, alignment=Qt.AlignCenter)

        buttons_layout.addWidget(manual_btn)
        buttons_layout.addWidget(auto_btn)
        content_layout.addWidget(buttons_container)

        # Kết nối sự kiện
        manual_btn.clicked.connect(self.showManualWatering)
        auto_btn.clicked.connect(self.showAutoWatering)

        content_layout.addStretch()

        # Navigation bar
        nav_bar = QWidget()
        nav_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setSpacing(10)

        nav_buttons = [
            ("🏠", self.get_translated_text('home'), lambda: self.showMainPage(self.current_user)),
            ("🌤", self.get_translated_text('weather'), self.showWeatherDetails),
            ("💧", self.get_translated_text('watering'), self.showWateringOptions),
            ("⚙️", self.get_translated_text('settings'), lambda: self.showSettingsPage(self.current_user))
        ]

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        for icon, tooltip, callback in nav_buttons:
            btn = QPushButton(icon)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setCheckable(True)
            btn.setToolTip(tooltip)
            if tooltip == self.get_translated_text('watering'):
                btn.setChecked(True)
            btn.clicked.connect(callback)
            nav_layout.addWidget(btn)
            self.button_group.addButton(btn)

        nav_bar.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
                padding: 10px;
            }
            QPushButton {
                border: none;
                border-radius: 10px;
                padding: 15px;
                font-size: 20px;
                background-color: #f0f0f0;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:checked {
                background-color: #4a90e2;
                color: white;
            }
        """)

        main_layout.addWidget(content_widget)
        main_layout.addWidget(nav_bar)

        self.setCentralWidget(watering_widget)
        self.current_page = watering_widget

    def showManualWatering(self):
        if self.current_page:
            self.current_page.deleteLater()

        manual_widget = QWidget()
        layout = QVBoxLayout(manual_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Tiêu đề
        title = QLabel(self.get_translated_text('manual_watering'))
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            margin: 10px 0;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 10px;
        """)
        layout.addWidget(title, alignment=Qt.AlignCenter)

        # Trạng thái
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        
        self.manual_status_icon = QLabel("🔴" if not self.manual_watering_on else "🟢")
        self.manual_status_icon.setStyleSheet("font-size: 48px;")
        
        self.manual_status_text = QLabel(
            self.get_translated_text('system_on') if self.manual_watering_on 
            else self.get_translated_text('system_off')
        )
        self.manual_status_text.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #f44336;
            padding: 20px;
            background-color: #f8f8f8;
            border-radius: 15px;
        """)
        
        status_layout.addWidget(self.manual_status_icon, alignment=Qt.AlignRight)
        status_layout.addWidget(self.manual_status_text, alignment=Qt.AlignLeft)
        layout.addWidget(status_widget)

        # Nút điều khiển
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        
        on_btn = QPushButton(f"🚿 {self.get_translated_text('on')}")
        off_btn = QPushButton(f"💧 {self.get_translated_text('off')}")

        for btn in [on_btn, off_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 20px;
                    padding: 20px;
                    min-width: 100px;
                    background-color: #4a90e2;
                    color: white;
                    border-radius: 15px;
                }
                QPushButton:hover {
                    background-color: #357ABD;
                }
            """)

        buttons_layout.addWidget(on_btn)
        buttons_layout.addWidget(off_btn)
        layout.addWidget(buttons_widget)

        # Nút quay lại
        back_btn = QPushButton(f"↩️ {self.get_translated_text('back')}")
        back_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 10px;
                background-color: #f0f0f0;
                border-radius: 10px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        layout.addWidget(back_btn)

        # Kết nối sự kiện
        on_btn.clicked.connect(self.turn_on_water)
        off_btn.clicked.connect(self.turn_off_water)
        back_btn.clicked.connect(self.showWateringOptions)

        layout.addStretch()

        # Navigation bar
        nav_bar = QWidget()
        nav_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setSpacing(10)

        nav_buttons = [
            ("🏠", self.get_translated_text('home'), lambda: self.showMainPage(self.current_user)),
            ("🌤", self.get_translated_text('weather'), self.showWeatherDetails),
            ("💧", self.get_translated_text('watering'), self.showWateringOptions),
            ("⚙️", self.get_translated_text('settings'), lambda: self.showSettingsPage(self.current_user))
        ]

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        for icon, tooltip, callback in nav_buttons:
            btn = QPushButton(icon)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setCheckable(True)
            btn.setToolTip(tooltip)
            if tooltip == self.get_translated_text('watering'):
                btn.setChecked(True)
            btn.clicked.connect(callback)
            nav_layout.addWidget(btn)
            self.button_group.addButton(btn)

        nav_bar.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
                padding: 10px;
            }
            QPushButton {
                border: none;
                border-radius: 10px;
                padding: 15px;
                font-size: 20px;
                background-color: #f0f0f0;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:checked {
                background-color: #4a90e2;
                color: white;
            }
        """)

        layout.addWidget(nav_bar)

        self.setCentralWidget(manual_widget)
        self.current_page = manual_widget

    def showAutoWatering(self):
        try:
            if self.current_page:
                self.current_page.deleteLater()

            auto_widget = QWidget()
            layout = QVBoxLayout(auto_widget)
            layout.setContentsMargins(30, 30, 30, 30)
            layout.setSpacing(25)

            # Scroll Area
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setStyleSheet("""
                QScrollArea {
                    border: none;
                    background-color: transparent;
                }
            """)

            content_widget = QWidget()
            content_layout = QVBoxLayout(content_widget)
            content_layout.setSpacing(25)

            # Tiêu đề
            title = QLabel(self.get_translated_text('auto_watering_title'))
            title.setStyleSheet("""
                font-size: 32px;
                font-weight: bold;
                color: #2E7D32;
                padding: 20px;
                background-color: white;
                border-radius: 15px;
                border: 2px solid #4CAF50;
            """)
            content_layout.addWidget(title, alignment=Qt.AlignCenter)

            # Trạng thái
            status_widget = QWidget()
            status_layout = QHBoxLayout(status_widget)
            status_layout.setContentsMargins(20, 20, 20, 20)
            
            self.auto_status_icon = QLabel("🔴" if not self.auto_watering_on else "🟢")
            self.auto_status_icon.setStyleSheet("font-size: 64px;")
            
            status_text = self.get_translated_text('auto_system_on' if self.auto_watering_on else 'auto_system_off')
            self.auto_status_text = QLabel(status_text)
            self.auto_status_text.setStyleSheet("""
                font-size: 28px;
                font-weight: bold;
                color: #f44336;
                padding: 25px;
                background-color: white;
                border: 2px solid #f44336;
                border-radius: 20px;
            """)
            
            status_layout.addWidget(self.auto_status_icon, alignment=Qt.AlignRight)
            status_layout.addWidget(self.auto_status_text, alignment=Qt.AlignLeft)
            content_layout.addWidget(status_widget)

            # Cài đặt
            settings_group = QGroupBox(self.get_translated_text('auto_watering_settings'))
            settings_group.setStyleSheet("""
                QGroupBox {
                    font-size: 28px;
                    font-weight: bold;
                    border: 3px solid #4CAF50;
                    border-radius: 20px;
                    margin-top: 30px;
                    padding: 20px;
                    background-color: white;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 20px;
                    padding: 0 15px;
                    background-color: white;
                    color: #2E7D32;
                }
            """)

            settings_layout = QFormLayout(settings_group)
            settings_layout.setSpacing(30)
            settings_layout.setContentsMargins(30, 50, 30, 30)
            settings_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

            # Style cho labels và controls
            label_style = """
                QLabel {
                    font-size: 24px;
                    font-weight: bold;
                    color: #333;
                    padding: 10px;
                }
            """
            control_style = """
                font-size: 22px;
                padding: 15px;
                border: 2px solid #4CAF50;
                border-radius: 10px;
                background-color: white;
                min-width: 150px;
            """

            # Thời gian bắt đầu
            start_label = QLabel(self.get_translated_text('start_time_label'))
            start_label.setStyleSheet(label_style)
            self.start_time = QTimeEdit()
            self.start_time.setTime(QTime(6, 0))
            self.start_time.setDisplayFormat("HH:mm")
            self.start_time.setStyleSheet(control_style)

            # Thời gian kết thúc
            end_label = QLabel(self.get_translated_text('end_time_label'))
            end_label.setStyleSheet(label_style)
            self.end_time = QTimeEdit()
            self.end_time.setTime(QTime(18, 0))
            self.end_time.setDisplayFormat("HH:mm")
            self.end_time.setStyleSheet(control_style)

            # Chu kỳ tưới
            cycle_label = QLabel(self.get_translated_text('cycle_label'))
            cycle_label.setStyleSheet(label_style)
            self.cycle_combo = QComboBox()
            cycles = ['cycle_30min', 'cycle_1hour', 'cycle_2hours', 'cycle_4hours']
            self.cycle_combo.addItems([self.get_translated_text(cycle) for cycle in cycles])
            self.cycle_combo.setStyleSheet(control_style)

            # Thời gian mỗi lần tưới
            duration_label = QLabel(self.get_translated_text('duration_label'))
            duration_label.setStyleSheet(label_style)
            self.duration_spin = QSpinBox()
            self.duration_spin.setRange(1, 30)
            self.duration_spin.setValue(5)
            self.duration_spin.setSuffix(f" {self.get_translated_text('minutes')}")
            self.duration_spin.setStyleSheet(control_style)

            # Thêm các widget vào form layout
            settings_layout.addRow(start_label, self.start_time)
            settings_layout.addRow(end_label, self.end_time)
            settings_layout.addRow(cycle_label, self.cycle_combo)
            settings_layout.addRow(duration_label, self.duration_spin)

            content_layout.addWidget(settings_group)

            # Thông tin cài đặt
            self.settings_info = QLabel()
            self.settings_info.setStyleSheet("""
                QLabel {
                    font-size: 22px;
                    color: #1B5E20;
                    padding: 20px;
                    background-color: #E8F5E9;
                    border: 2px solid #4CAF50;
                    border-radius: 15px;
                    margin: 20px 0;
                    line-height: 1.5;
                }
            """)
            self.settings_info.hide()
            content_layout.addWidget(self.settings_info)

            # Nút điều khiển
            buttons_widget = QWidget()
            buttons_layout = QHBoxLayout(buttons_widget)
            buttons_layout.setSpacing(20)

            # Nút trở về
            back_btn = QPushButton(self.get_translated_text('back_btn'))
            back_btn.setStyleSheet("""
                QPushButton {
                    background-color: #757575;
                    color: white;
                    padding: 15px 30px;
                    border-radius: 12px;
                    font-size: 24px;
                    min-width: 150px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #616161;
                }
            """)

            enable_btn = QPushButton(self.get_translated_text('activate_btn'))
            disable_btn = QPushButton(self.get_translated_text('deactivate_btn'))

            button_style = """
                QPushButton {{
                    background-color: {};
                    color: white;
                    padding: 15px 30px;
                    border-radius: 12px;
                    font-size: 24px;
                    min-width: 180px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {};
                }}
            """

            enable_btn.setStyleSheet(button_style.format("#4CAF50", "#45a049"))
            disable_btn.setStyleSheet(button_style.format("#f44336", "#da190b"))

            buttons_layout.addWidget(back_btn)
            buttons_layout.addWidget(enable_btn)
            buttons_layout.addWidget(disable_btn)
            content_layout.addWidget(buttons_widget)

            # Thêm widget content vào scroll area
            scroll.setWidget(content_widget)
            layout.addWidget(scroll)

            # Kết nối sự kiện
            back_btn.clicked.connect(self.showWateringOptions)
            enable_btn.clicked.connect(self.enable_auto_watering)
            disable_btn.clicked.connect(self.disable_auto_watering)

            # Thêm navigation bar
            self.addNavigationBar(layout, self.get_translated_text('watering'))

            # Đặt kích thước tối thiểu cho widget
            auto_widget.setMinimumSize(800, 1000)
            
            self.setCentralWidget(auto_widget)
            self.current_page = auto_widget

            # Cập nhật trạng thái dựa trên biến đã lưu
            if self.auto_watering_on and self.auto_watering_settings:
                self.auto_status_icon.setText("🟢")
                self.auto_status_text.setText(self.get_translated_text('auto_system_on'))
                self.auto_status_text.setStyleSheet("""
                    font-size: 24px;
                    font-weight: bold;
                    color: #4CAF50;
                    padding: 20px;
                    background-color: #f8f8f8;
                    border-radius: 15px;
                """)
                
                # Khôi phục các cài đặt
                self.start_time.setTime(QTime.fromString(self.auto_watering_settings['start_time'], 'HH:mm'))
                self.end_time.setTime(QTime.fromString(self.auto_watering_settings['end_time'], 'HH:mm'))
                
                # Tìm và đặt chu kỳ tưới phù hợp
                current_cycle = self.auto_watering_settings['cycle']
                for i in range(self.cycle_combo.count()):
                    if self.cycle_combo.itemText(i) == current_cycle:
                        self.cycle_combo.setCurrentIndex(i)
                        break
                
                self.duration_spin.setValue(self.auto_watering_settings['duration'])
                
                # Hiển thị thông tin cài đặt
                settings_text = f"""
{self.get_translated_text('operating_time')} {self.auto_watering_settings['start_time']} - {self.auto_watering_settings['end_time']}
{self.get_translated_text('watering_cycle')} {current_cycle}
{self.get_translated_text('watering_duration')} {self.auto_watering_settings['duration']} {self.get_translated_text('minutes')}
                """
                self.settings_info.setText(settings_text)
                self.settings_info.show()

        except Exception as e:
            print(f"Lỗi trong showAutoWatering: {str(e)}")

    def showSettingsPage(self, username):
        if self.current_page:
            self.current_page.deleteLater()

        settings_widget = QWidget()
        main_layout = QVBoxLayout(settings_widget)

        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Tiêu đề
        title = QLabel(self.get_translated_text('settings'))
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        content_layout.addWidget(title, alignment=Qt.AlignCenter)

        # Danh sách các nút cài đặt
        settings_buttons = [
            ("👤", self.get_translated_text('personal_info'), lambda: self.showUserInfoDialog(username)),
            ("🔔", self.get_translated_text('notifications'), lambda: QMessageBox.information(self, self.get_translated_text('notifications'), "Tính năng đang phát triển")),
            ("🌍", self.get_translated_text('language'), lambda: self.showLanguagePage()),
            ("🔌", self.get_translated_text('pin'), lambda: QMessageBox.information(self, self.get_translated_text('pin'), "Tính năng đang phát triển")),
            ("❓", self.get_translated_text('help'), lambda: QMessageBox.information(self, self.get_translated_text('help'), "Tính năng đang phát triển")),
        ]

        for icon, text, callback in settings_buttons:
            btn = QPushButton(f"{icon} {text}")
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 15px;
                    font-size: 16px;
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    margin: 5px 0;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                }
            """)
            btn.clicked.connect(callback)
            content_layout.addWidget(btn)

        # Thêm khoảng trống
        content_layout.addStretch()

        # Phiên bản
        version_label = QLabel(self.get_translated_text('version'))
        version_label.setStyleSheet("color: #666; font-size: 12px;")
        content_layout.addWidget(version_label, alignment=Qt.AlignCenter)

        # Thêm content widget vào main layout
        main_layout.addWidget(content_widget)

        # Navigation bar
        nav_bar = QWidget()
        nav_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setSpacing(10)

        nav_buttons = [
            ("🏠", self.get_translated_text('home'), lambda: self.showMainPage(username)),
            ("🌤", self.get_translated_text('weather'), self.showWeatherDetails),
            ("💧", self.get_translated_text('watering'), self.showWateringOptions),
            ("⚙️", self.get_translated_text('settings'), lambda: None)
        ]

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        for icon, tooltip, callback in nav_buttons:
            btn = QPushButton(icon)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setCheckable(True)
            btn.setToolTip(tooltip)
            if tooltip == self.get_translated_text('settings'):
                btn.setChecked(True)
            btn.clicked.connect(callback)
            nav_layout.addWidget(btn)
            self.button_group.addButton(btn)

        nav_bar.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
                padding: 10px;
            }
            QPushButton {
                border: none;
                border-radius: 10px;
                padding: 15px;
                font-size: 20px;
                background-color: #f0f0f0;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:checked {
                background-color: #4a90e2;
                color: white;
            }
        """)

        main_layout.addWidget(nav_bar)

        self.setCentralWidget(settings_widget)
        self.current_page = settings_widget

    def showUserInfoDialog(self, username):
        dialog = QDialog(self)
        dialog.setWindowTitle("Thông tin cá nhân")
        dialog.setFixedWidth(400)
        layout = QVBoxLayout(dialog)

        # Form thông tin
        form_widget = QWidget()
        form_layout = QGridLayout(form_widget)

        # Email hiện tại
        current_email = self.users_db[username]["email"]

        # Các trường nhập liệu
        labels = ["Email:", "Mật khẩu hiện tại:", "Mật khẩu mới:", "Xác nhận mật khẩu mới:"]
        self.settings_inputs = {}

        for i, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 14px; font-weight: bold;")
            input_field = QLineEdit()
            input_field.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    font-size: 14px;
                }
            """)
            
            if label_text == "Email:":
                input_field.setText(current_email)
            
            if "mật khẩu" in label_text.lower():
                input_field.setEchoMode(QLineEdit.Password)
            
            form_layout.addWidget(label, i, 0)
            form_layout.addWidget(input_field, i, 1)
            self.settings_inputs[label_text] = input_field

        layout.addWidget(form_widget)

        # Nút điều khiển
        buttons_layout = QHBoxLayout()
        
        save_btn = QPushButton("Lưu thay đổi")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        cancel_btn = QPushButton("Hủy")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)

        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)

        layout.addLayout(buttons_layout)

        # Kết nối các sự kiện
        save_btn.clicked.connect(lambda: self.saveUserSettings(username, dialog))
        cancel_btn.clicked.connect(dialog.reject)

        dialog.exec_()

    def saveUserSettings(self, username, dialog=None):
        email = self.settings_inputs["Email:"].text().strip()
        current_password = self.settings_inputs["Mật khẩu hiện tại:"].text().strip()
        new_password = self.settings_inputs["Mật khẩu mới:"].text().strip()
        confirm_password = self.settings_inputs["Xác nhận mật khẩu mới:"].text().strip()

        if current_password != self.users_db[username]["password"]:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu hiện tại không đúng!")
            return

        if not self.isValidEmail(email):
            QMessageBox.warning(self, "Lỗi", "Email không hợp lệ!")
            return

        if new_password:
            if len(new_password) < 4:
                QMessageBox.warning(self, "Lỗi", "Mật khẩu mới phải có ít nhất 4 ký tự!")
                return
            if new_password != confirm_password:
                QMessageBox.warning(self, "Lỗi", "Mật khẩu mới không khớp!")
                return
            self.users_db[username]["password"] = new_password

        self.users_db[username]["email"] = email

        QMessageBox.information(self, "Thành công", "Đã cập nhật thông tin tài khoản!")
        if dialog:
            dialog.accept()

    def isValidEmail(self, email):
        import re
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def turn_on_water(self):
        self.manual_watering_on = True
        self.manual_status_icon.setText("🟢")
        self.manual_status_text.setText(self.get_translated_text('system_on'))
        self.manual_status_text.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
            padding: 20px;
            background-color: #f8f8f8;
            border-radius: 15px;
        """)

    def turn_off_water(self):
        self.manual_watering_on = False
        self.manual_status_icon.setText("🔴")
        self.manual_status_text.setText(self.get_translated_text('system_off'))
        self.manual_status_text.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #f44336;
            padding: 20px;
            background-color: #f8f8f8;
            border-radius: 15px;
        """)

    def enable_auto_watering(self):
        try:
            self.auto_watering_on = True
            # Lưu các cài đặt hiện tại
            self.auto_watering_settings = {
                'start_time': self.start_time.time().toString('HH:mm'),
                'end_time': self.end_time.time().toString('HH:mm'),
                'cycle': self.cycle_combo.currentText(),
                'duration': self.duration_spin.value()
            }
            
            self.auto_status_icon.setText("🟢")
            self.auto_status_text.setText(self.get_translated_text('auto_system_on'))
            self.auto_status_text.setStyleSheet("""
                font-size: 24px;
                font-weight: bold;
                color: #4CAF50;
                padding: 20px;
                background-color: #f8f8f8;
                border-radius: 15px;
            """)
            
            settings_text = f"""
{self.get_translated_text('operating_time')} {self.auto_watering_settings['start_time']} - {self.auto_watering_settings['end_time']}
{self.get_translated_text('watering_cycle')} {self.auto_watering_settings['cycle']}
{self.get_translated_text('watering_duration')} {self.auto_watering_settings['duration']} {self.get_translated_text('minutes')}
            """
            self.settings_info.setText(settings_text)
            self.settings_info.show()
        except Exception as e:
            print(f"Lỗi trong enable_auto_watering: {str(e)}")

    def disable_auto_watering(self):
        try:
            self.auto_watering_on = False
            self.auto_watering_settings = None
            
            self.auto_status_icon.setText("🔴")
            self.auto_status_text.setText(self.get_translated_text('auto_system_off'))
            self.auto_status_text.setStyleSheet("""
                font-size: 24px;
                font-weight: bold;
                color: #f44336;
                padding: 20px;
                background-color: #f8f8f8;
                border-radius: 15px;
            """)
            self.settings_info.hide()
        except Exception as e:
            print(f"Lỗi trong disable_auto_watering: {str(e)}")

    def addNavigationBar(self, layout, current_page):
        """
        Hàm chung để thêm navigation bar vào layout
        current_page: tên của trang hiện tại ("home", "weather", "water", "settings")
        """
        nav_bar = QWidget()
        nav_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setSpacing(10)

        nav_buttons = [
            ("🏠", "Trang chủ", lambda: self.showMainPage(self.current_user)),
            ("🌤", "Thời tiết", self.showWeatherDetails),
            ("💧", "Tưới nước", self.showWateringOptions),
            ("⚙️", "Cài đặt", lambda: self.showSettingsPage(self.current_user))
        ]

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        for icon, tooltip, callback in nav_buttons:
            btn = QPushButton(icon)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setCheckable(True)
            btn.setToolTip(tooltip)
            if tooltip == current_page:
                btn.setChecked(True)
            btn.clicked.connect(callback)
            nav_layout.addWidget(btn)
            self.button_group.addButton(btn)

        nav_bar.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
                padding: 10px;
            }
            QPushButton {
                border: none;
                border-radius: 10px;
                padding: 15px;
                font-size: 20px;
                background-color: #f0f0f0;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:checked {
                background-color: #4a90e2;
                color: white;
            }
        """)

        layout.addWidget(nav_bar)

    def showLanguagePage(self):
        if self.current_page:
            self.current_page.deleteLater()

        language_widget = QWidget()
        main_layout = QVBoxLayout(language_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Tiêu đề
        title = QLabel(self.get_translated_text('select_language'))
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #2E7D32;
            padding: 20px;
            background-color: white;
            border-radius: 15px;
            border: 2px solid #4CAF50;
        """)
        content_layout.addWidget(title, alignment=Qt.AlignCenter)

        # Container cho các nút chọn ngôn ngữ
        language_container = QWidget()
        language_layout = QVBoxLayout(language_container)
        language_layout.setSpacing(15)

        # Danh sách các nút chọn ngôn ngữ
        for lang, name in self.languages.items():
            btn = QPushButton(name)
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 20px;
                    font-size: 18px;
                    background-color: white;
                    border: 2px solid #ddd;
                    border-radius: 12px;
                    margin: 5px 0;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                }
            """)
            
            if lang == self.current_language:
                btn.setStyleSheet(btn.styleSheet() + """
                    QPushButton {
                        background-color: #e3f2fd;
                        border: 2px solid #2196f3;
                    }
                """)
            
            btn.clicked.connect(lambda checked, l=lang: self.changeLanguage(l))
            language_layout.addWidget(btn)

        content_layout.addWidget(language_container)

        # Thêm khoảng trống
        content_layout.addStretch()

        # Nút quay lại
        back_btn = QPushButton("↩️ " + self.get_translated_text('back'))
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                padding: 15px 30px;
                border-radius: 12px;
                font-size: 18px;
                min-width: 150px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        back_btn.clicked.connect(lambda: self.showSettingsPage(self.current_user))
        content_layout.addWidget(back_btn, alignment=Qt.AlignCenter)

        # Thêm content widget vào main layout
        main_layout.addWidget(content_widget)

        # Navigation bar
        nav_bar = QWidget()
        nav_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setSpacing(10)

        nav_buttons = [
            ("🏠", self.get_translated_text('home'), lambda: self.showMainPage(self.current_user)),
            ("🌤", self.get_translated_text('weather'), self.showWeatherDetails),
            ("💧", self.get_translated_text('watering'), self.showWateringOptions),
            ("⚙️", self.get_translated_text('settings'), lambda: self.showSettingsPage(self.current_user))
        ]

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        for icon, tooltip, callback in nav_buttons:
            btn = QPushButton(icon)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setCheckable(True)
            btn.setToolTip(tooltip)
            if tooltip == self.get_translated_text('settings'):
                btn.setChecked(True)
            btn.clicked.connect(callback)
            nav_layout.addWidget(btn)
            self.button_group.addButton(btn)

        nav_bar.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 5px;
                font-size: 10px;
                background-color: #f0f0f0;
                min-width: 30px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:checked {
                background-color: #4a90e2;
                color: white;
            }
        """)

        main_layout.addWidget(nav_bar)

        self.setCentralWidget(language_widget)
        self.current_page = language_widget

    def changeLanguage(self, lang):
        try:
            # Cập nhật ngôn ngữ hiện tại
            self.current_language = lang
            
            # Xác định trang hiện tại
            current_page = None
            if hasattr(self, 'button_group') and self.button_group:
                checked_button = self.button_group.checkedButton()
                if checked_button:
                    current_page = checked_button.toolTip()

            # Cập nhật giao diện với ngôn ngữ mới
            if self.current_user:
                # Tải lại trang hiện tại với ngôn ngữ mới
                if current_page == self.get_translated_text('home'):
                    self.showMainPage(self.current_user)
                elif current_page == self.get_translated_text('weather'):
                    self.showWeatherDetails()
                elif current_page == self.get_translated_text('watering'):
                    self.showWateringOptions()
                elif current_page == self.get_translated_text('settings'):
                    self.showSettingsPage(self.current_user)
                else:
                    # Mặc định quay về trang cài đặt
                    self.showSettingsPage(self.current_user)
            else:
                # Nếu chưa đăng nhập, cập nhật trang đăng nhập
                self.showLoginPage()

            # Hiển thị thông báo
            QMessageBox.information(
                self,
                self.get_translated_text('success'),
                f"{self.get_translated_text('language_changed')} {self.languages[lang]}"
            )

        except Exception as e:
            print(f"Lỗi khi thay đổi ngôn ngữ: {str(e)}")
            QMessageBox.critical(
                self,
                self.get_translated_text('error'),
                f"Đã xảy ra lỗi khi thay đổi ngôn ngữ: {str(e)}"
            )

    def updateUI(self):
        """Update all UI elements with new language"""
        try:
            # Cập nhật tiêu đề cửa sổ
            self.setWindowTitle(self.get_translated_text('app_title'))
            
            # Nếu đang ở trang đăng nhập, cập nhật lại toàn bộ trang đăng nhập
            if isinstance(self.current_page, QWidget) and self.current_page.layout():
                if self.username_input and self.password_input:
                    self.username_input.setPlaceholderText(self.get_translated_text('username'))
                    self.password_input.setPlaceholderText(self.get_translated_text('password'))
                        
                    # Cập nhật các label khác trên trang đăng nhập
                    for child in self.current_page.findChildren(QLabel):
                        if child.text() == "Đăng nhập":
                            child.setText(self.get_translated_text('login'))
                        elif child.text() == "Hệ thống quản lý nông nghiệp":
                            child.setText(self.get_translated_text('system_title'))
                        elif child.text() == "Hiển thị mật khẩu":
                            child.setText(self.get_translated_text('show_password'))
                        
                    # Cập nhật nút đăng nhập
                    for child in self.current_page.findChildren(QPushButton):
                        if child.text() == "Đăng nhập":
                            child.setText(self.get_translated_text('login'))
            
            # Nếu đang ở trang cài đặt, cập nhật lại toàn bộ trang cài đặt
            if self.current_user:
                # Kiểm tra xem đang ở trang nào
                if hasattr(self, 'button_group') and self.button_group:
                    # Lấy nút đang được chọn
                    checked_button = self.button_group.checkedButton()
                    if checked_button:
                        # Lấy tooltip của nút để xác định trang hiện tại
                        current_page = checked_button.toolTip()
                        
                        # Cập nhật trang tương ứng
                        if current_page == self.get_translated_text('home'):
                            self.showMainPage(self.current_user)
                        elif current_page == self.get_translated_text('weather'):
                            self.showWeatherDetails()
                        elif current_page == self.get_translated_text('watering'):
                            self.showWateringOptions()
                        elif current_page == self.get_translated_text('settings'):
                            self.showSettingsPage(self.current_user)
                else:
                    # Nếu không có button_group, mặc định là trang cài đặt
                    self.showSettingsPage(self.current_user)
                    
        except Exception as e:
            print(f"Lỗi khi cập nhật giao diện: {str(e)}")

    def get_translated_text(self, key):
        """Get translated text based on current language"""
        if self.current_language == "auto":
            # Get system language
            system_language = QLocale.system().language()
            if system_language == QLocale.Vietnamese:
                lang = "vi"
            else:
                lang = "en"
        else:
            lang = self.current_language
            
        return self.translations[lang].get(key, key)

    def logout(self):
        # Dừng timer trước khi logout
        if self.timer:
            self.timer.stop()
            self.timer.deleteLater()
            self.timer = None
        self.current_user = None  # Reset current_user khi logout
        self.showLoginPage()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle('Fusion')

    # Set global stylesheet
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

