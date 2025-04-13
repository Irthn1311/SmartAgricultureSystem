import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QCheckBox, QFileDialog,
    QMessageBox, QFrame, QSizePolicy, QButtonGroup, QGridLayout  # <- thêm QGridLayout ở đây
)


class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.icon_path = "weather.ico"
        self.setWindowIcon(QIcon(self.icon_path))
        self.users_db = {
            "user1": {"password": "1111", "email": "user1@example.com"},
            "user2": {"password": "2222", "email": "user2@example.com"},
            "user3": {"password": "3333", "email": "user3@example.com"},
            "user4": {"password": "4444", "email": "user4@example.com"},
            "user5": {"password": "5555", "email": "user5@example.com"},
        }
        self.timer = None  # Khởi tạo timer là None
        self.current_user = None  # Thêm biến current_user
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ứng dụng Thời tiết')
        self.setMinimumSize(600, 800)
        self.current_page = None
        self.showLoginPage()

    def showLoginForm(self):
        self.showMainPage()

    def showLoginPage(self):
        if self.current_page:
            self.current_page.deleteLater()

        login_widget = QWidget()
        layout = QVBoxLayout()

        # Tiêu đề
        app_name = QLabel("Hệ thống quản lý nông nghiệp")
        app_name.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(app_name, alignment=Qt.AlignCenter)

        # Ô nhập
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.username_input.setPlaceholderText("Tên đăng nhập")
        self.password_input.setPlaceholderText("Mật khẩu")
        self.password_input.setEchoMode(QLineEdit.Password)

        show_password_cb = QCheckBox("Hiển thị mật khẩu")
        show_password_cb.stateChanged.connect(self.togglePasswordVisibility)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(show_password_cb)

        # Nút đăng nhập
        login_btn = QPushButton("Đăng nhập")
        login_btn.setStyleSheet("background-color: #4a90e2; color: white; padding: 10px; min-width: 200px;")
        login_btn.clicked.connect(self.handleLogin)
        layout.addWidget(login_btn, alignment=Qt.AlignCenter)

        # Label hiển thị thông báo
        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message_label)

        login_widget.setLayout(layout)
        self.setCentralWidget(login_widget)
        self.current_page = login_widget

    def togglePasswordVisibility(self, state):
        if state == Qt.Checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

    def handleLogin(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.message_label.setText("Vui lòng nhập đầy đủ thông tin!")
            self.message_label.setStyleSheet("color: red;")
            return

        if username not in self.users_db or self.users_db[username]["password"] != password:
            self.message_label.setText("Tên đăng nhập hoặc mật khẩu không đúng!")
            self.message_label.setStyleSheet("color: red;")
            return

        self.current_user = username  # Lưu username hiện tại
        self.message_label.setText("Đăng nhập thành công!")
        self.message_label.setStyleSheet("color: green;")
        QTimer.singleShot(1000, lambda: self.showMainPage(username))

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
        # Logout Button
        logout_btn = QPushButton("Đăng xuất")
        logout_btn.clicked.connect(self.logout)
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
            ("🌡", "Nhiệt độ:", "**", "°C"),
            ("💨", "Sức gió:", "**", "km/h"),
            ("💧", "Độ ẩm:", "**", "%"),
            ("🏗", "Kết tủa:", "**", "%")
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
            ("🏠", "Trang chủ"),
            ("🌤", "Thời tiết"),
            ("💧", "Tưới nước"),
            ("⚙️", "Cài đặt")
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

        # Kết nối sự kiện click vào nút thời tiết
        self.button_group.buttons()[1].clicked.connect(self.showWeatherDetails)
        # Kết nối sự kiện click vào nút tưới nước
        self.button_group.buttons()[2].clicked.connect(self.showWateringOptions)
        # Kết nối sự kiện click vào nút cài đặt
        self.button_group.buttons()[3].clicked.connect(lambda: self.showSettingsPage(username))

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

    def updateDateTime(self):
        try:
            if hasattr(self, 'time_label') and self.time_label and not self.time_label.isHidden():
                current = QDateTime.currentDateTime()
                self.time_label.setText(current.toString("HH:mm"))

                # Chuyển đổi thứ sang tiếng Việt
                day_map = {
                    1: "Thứ Hai",
                    2: "Thứ Ba",
                    3: "Thứ Tư",
                    4: "Thứ Năm",
                    5: "Thứ Sáu",
                    6: "Thứ Bảy",
                    0: "Chủ Nhật"
                }

                weekday = current.date().dayOfWeek() % 7
                date_str = f"{day_map[weekday]}, {current.toString('dd-MM-yyyy')}"
                if hasattr(self, 'date_label') and self.date_label:
                    self.date_label.setText(date_str)
        except RuntimeError:
            # Nếu widget đã bị xóa, dừng timer
            if self.timer:
                self.timer.stop()
                self.timer.deleteLater()
                self.timer = None

    def showWeatherDetails(self):
        self.fetchWeatherData()
        # ... (các phần code khác)

    def fetchWeatherData(self):
        # API key từ OpenWeatherMap - đảm bảo đã được kích hoạt
        api_key = "4b491ab9f64944de56b3167c89d73ad0"  # API key mới
        # Tọa độ của Hồ Chí Minh
        lat = 10.8231
        lon = 106.6297
        
        if not api_key or api_key == "YOUR_API_KEY":
            QMessageBox.warning(self, "Lỗi", "Vui lòng cập nhật API key!")
            return

        weather_data = self.get_weather_data(api_key, lat, lon)
        if weather_data:
            try:
                temperature = round(weather_data["main"]["temp"])
                humidity = weather_data["main"]["humidity"]
                wind_speed = round(weather_data["wind"]["speed"] * 3.6, 1)
                description = weather_data["weather"][0]["description"]

                # Cập nhật giao diện người dùng với dữ liệu thời tiết
                if hasattr(self, 'params'):
                    self.params[0] = ("🌡", "Nhiệt độ:", f"{temperature}", "°C")
                    self.params[1] = ("💨", "Sức gió:", f"{wind_speed}", "km/h")
                    self.params[2] = ("💧", "Độ ẩm:", f"{humidity}", "%")
                    self.params[3] = ("🏗", "Kết tủa:", "0", "%")

                if hasattr(self, 'weather_text') and self.weather_text:
                    self.weather_text.setText(description.capitalize())
                if hasattr(self, 'weather_icon') and self.weather_icon:
                    if "nắng" in description.lower():
                        self.weather_icon.setText("☀️")
                    elif "mưa" in description.lower():
                        self.weather_icon.setText("🌧️")
                    elif "mây" in description.lower():
                        self.weather_icon.setText("☁️")
                    else:
                        self.weather_icon.setText("🌤️")

                params_grid = self.findChild(QGridLayout)
                if params_grid:
                    for i, (icon, label, value, unit) in enumerate(self.params):
                        param_widget = params_grid.itemAtPosition(i // 2, (i % 2) * 2).widget()
                        if param_widget and not param_widget.isHidden():
                            right = param_widget.layout().itemAt(2).widget()
                            if right and not right.isHidden():
                                right.setText(f"{value}{unit}")

            except Exception as e:
                print(f"Lỗi khi cập nhật giao diện thời tiết: {str(e)}")
                QMessageBox.warning(self, "Lỗi", "Không thể cập nhật thông tin thời tiết.")
        else:
            error_msg = """Không thể lấy dữ liệu thời tiết. Có thể do:
1. API key chưa được kích hoạt (cần đợi vài giờ sau khi đăng ký)
2. API key không hợp lệ
3. Vấn đề về kết nối mạng

Vui lòng kiểm tra lại!"""
            QMessageBox.warning(self, "Lỗi", error_msg)

    def get_weather_data(self, api_key, lat, lon):
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric",  # Lấy nhiệt độ theo độ Celsius
            "lang": "vi"  # Lấy thông tin thời tiết bằng tiếng Việt
        }

        try:
            response = requests.get(base_url, params=params, timeout=10)
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

    def logout(self):
        # Dừng timer trước khi logout
        if self.timer:
            self.timer.stop()
            self.timer.deleteLater()
            self.timer = None
        self.current_user = None  # Reset current_user khi logout
        self.showLoginPage()

    def showWateringOptions(self):
        if self.current_page:
            self.current_page.deleteLater()

        watering_widget = QWidget()
        main_layout = QVBoxLayout(watering_widget)

        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        title = QLabel("Chế độ tưới nước")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        content_layout.addWidget(title, alignment=Qt.AlignCenter)

        manual_btn = QPushButton("Tưới thủ công")
        auto_btn = QPushButton("Tưới tự động")

        for btn in [manual_btn, auto_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 18px;
                    padding: 12px;
                    background-color: #4a90e2;
                    color: white;
                    border-radius: 10px;
                    margin: 5px 0;
                }
                QPushButton:hover {
                    background-color: #357ABD;
                }
            """)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        manual_btn.clicked.connect(self.showManualWatering)
        auto_btn.clicked.connect(self.showAutoWateringDialog)

        content_layout.addWidget(manual_btn)
        content_layout.addWidget(auto_btn)
        content_layout.addStretch()

        # Thêm content widget vào main layout
        main_layout.addWidget(content_widget)

        # Navigation bar
        nav_bar = QWidget()
        nav_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setSpacing(10)

        nav_buttons = [
            ("🏠", "Trang chủ", lambda: self.showMainPage(self.current_user)),
            ("🌤", "Thời tiết", self.showWeatherDetails),
            ("💧", "Tưới nước", lambda: None),  # Đang ở trang tưới nước
            ("⚙️", "Cài đặt", lambda: self.showSettingsPage(self.current_user))
        ]

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        for icon, tooltip, callback in nav_buttons:
            btn = QPushButton(icon)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setCheckable(True)
            btn.setToolTip(tooltip)
            if tooltip == "Tưới nước":  # Highlight nút tưới nước
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

        self.setCentralWidget(watering_widget)
        self.current_page = watering_widget

    def showAutoWateringDialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Tưới tự động")
        dialog.setFixedWidth(400)
        layout = QVBoxLayout(dialog)

        # Tiêu đề
        title = QLabel("Chế độ tưới tự động")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        # Các tùy chọn cài đặt
        settings_widget = QWidget()
        settings_layout = QFormLayout(settings_widget)

        # Thời gian bắt đầu
        start_time = QTimeEdit()
        start_time.setTime(QTime(6, 0))  # Mặc định 6:00
        start_time.setDisplayFormat("HH:mm")
        settings_layout.addRow("Thời gian bắt đầu:", start_time)

        # Thời gian kết thúc
        end_time = QTimeEdit()
        end_time.setTime(QTime(18, 0))  # Mặc định 18:00
        end_time.setDisplayFormat("HH:mm")
        settings_layout.addRow("Thời gian kết thúc:", end_time)

        # Chu kỳ tưới
        cycle_combo = QComboBox()
        cycle_combo.addItems(["30 phút", "1 giờ", "2 giờ", "4 giờ"])
        settings_layout.addRow("Chu kỳ tưới:", cycle_combo)

        # Thời gian tưới mỗi lần
        duration_spin = QSpinBox()
        duration_spin.setRange(1, 30)
        duration_spin.setValue(5)
        duration_spin.setSuffix(" phút")
        settings_layout.addRow("Thời gian mỗi lần tưới:", duration_spin)

        layout.addWidget(settings_widget)

        # Nút điều khiển
        buttons_layout = QHBoxLayout()
        
        enable_btn = QPushButton("Kích hoạt")
        enable_btn.setStyleSheet("""
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

        buttons_layout.addWidget(enable_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addLayout(buttons_layout)

        # Kết nối sự kiện
        enable_btn.clicked.connect(lambda: self.enableAutoWatering(
            start_time.time(),
            end_time.time(),
            cycle_combo.currentText(),
            duration_spin.value(),
            dialog
        ))
        cancel_btn.clicked.connect(dialog.reject)

        dialog.exec_()

    def enableAutoWatering(self, start_time, end_time, cycle, duration, dialog):
        message = f"""Đã kích hoạt tưới tự động với các thông số:
- Thời gian bắt đầu: {start_time.toString('HH:mm')}
- Thời gian kết thúc: {end_time.toString('HH:mm')}
- Chu kỳ tưới: {cycle}
- Thời gian mỗi lần tưới: {duration} phút"""
        
        QMessageBox.information(self, "Thành công", message)
        dialog.accept()

    def showManualWatering(self):
        if self.current_page:
            self.current_page.deleteLater()

        manual_widget = QWidget()
        main_layout = QVBoxLayout(manual_widget)

        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        title = QLabel("Chế độ tưới thủ công")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        content_layout.addWidget(title, alignment=Qt.AlignCenter)

        on_btn = QPushButton("🚿 Bật nước")
        off_btn = QPushButton("💧 Tắt nước")

        for btn in [on_btn, off_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 18px;
                    padding: 12px;
                    background-color: #4a90e2;
                    color: white;
                    border-radius: 10px;
                    margin: 5px 0;
                }
                QPushButton:hover {
                    background-color: #357ABD;
                }
            """)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        on_btn.clicked.connect(lambda: QMessageBox.information(self, "Thông báo", "💧 Hệ thống tưới đã được **BẬT**!"))
        off_btn.clicked.connect(lambda: QMessageBox.information(self, "Thông báo", "🚫 Hệ thống tưới đã được **TẮT**!"))

        content_layout.addWidget(on_btn)
        content_layout.addWidget(off_btn)
        content_layout.addStretch()

        # Thêm content widget vào main layout
        main_layout.addWidget(content_widget)

        # Navigation bar
        nav_bar = QWidget()
        nav_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setSpacing(10)

        nav_buttons = [
            ("🏠", "Trang chủ", lambda: self.showMainPage(self.current_user)),
            ("🌤", "Thời tiết", self.showWeatherDetails),
            ("💧", "Tưới nước", lambda: self.showWateringOptions()),
            ("⚙️", "Cài đặt", lambda: self.showSettingsPage(self.current_user))
        ]

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        for icon, tooltip, callback in nav_buttons:
            btn = QPushButton(icon)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setCheckable(True)
            btn.setToolTip(tooltip)
            if tooltip == "Tưới nước":  # Highlight nút tưới nước
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

        self.setCentralWidget(manual_widget)
        self.current_page = manual_widget

    def showSettingsPage(self, username):
        if self.current_page:
            self.current_page.deleteLater()

        settings_widget = QWidget()
        main_layout = QVBoxLayout(settings_widget)

        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Tiêu đề
        title = QLabel("Cài đặt hệ thống")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        content_layout.addWidget(title, alignment=Qt.AlignCenter)

        # Danh sách các nút cài đặt
        settings_buttons = [
            ("👤 Thông tin cá nhân", lambda: self.showUserInfoDialog(username)),
            ("🔔 Thông báo", lambda: QMessageBox.information(self, "Thông báo", "Tính năng đang phát triển")),
            ("🌍 Ngôn ngữ", lambda: QMessageBox.information(self, "Thông báo", "Tính năng đang phát triển")),
            ("🎨 Giao diện", lambda: QMessageBox.information(self, "Thông báo", "Tính năng đang phát triển")),
            ("⚡ Hiệu suất", lambda: QMessageBox.information(self, "Thông báo", "Tính năng đang phát triển")),
            ("❓ Trợ giúp", lambda: QMessageBox.information(self, "Thông báo", "Tính năng đang phát triển")),
        ]

        for text, callback in settings_buttons:
            btn = QPushButton(text)
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
        version_label = QLabel("Phiên bản 1.0.0")
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
            ("🏠", "Trang chủ", lambda: self.showMainPage(username)),
            ("🌤", "Thời tiết", self.showWeatherDetails),
            ("💧", "Tưới nước", self.showWateringOptions),
            ("⚙️", "Cài đặt", lambda: None)  # Không làm gì khi đã ở trang Settings
        ]

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        for icon, tooltip, callback in nav_buttons:
            btn = QPushButton(icon)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setCheckable(True)
            btn.setToolTip(tooltip)
            if tooltip == "Cài đặt":  # Highlight nút Settings
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

    