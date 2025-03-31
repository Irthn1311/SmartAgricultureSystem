import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import re
import json

class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.icon_path = r"C:\Users\Admin\Downloads\SenseFarm\weather\weather.ico"
        self.setWindowIcon(QIcon(self.icon_path))
        self.users_db = {}
        self.load_users()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ứng dụng Thời tiết')
        self.setMinimumSize(400, 600)
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

        # Dòng chữ "Chưa có tài khoản?" + Đăng ký
        register_layout = QHBoxLayout()
        no_account_label = QLabel("Chưa có tài khoản?")
        register_label = QLabel("<a href='#'>Đăng ký</a>")
        register_label.setStyleSheet("color: red; font-weight: bold;")
        register_label.setCursor(Qt.PointingHandCursor)
        register_label.linkActivated.connect(self.showRegisterPage)

        register_layout.addWidget(no_account_label)
        register_layout.addWidget(register_label)
        register_layout.addStretch()

        layout.addLayout(register_layout)

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
            QMessageBox.warning(self, "Lỗi đăng nhập", "Vui lòng nhập đầy đủ thông tin!")
            return

        if username not in self.users_db or self.users_db[username]["password"] != password:
            QMessageBox.warning(self, "Lỗi đăng nhập", "Tên đăng nhập hoặc mật khẩu không đúng!")
            return

        self.showMainPage(username)

    def showRegisterPage(self):
        if self.current_page:
            self.current_page.deleteLater()

        register_widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Đăng ký tài khoản")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        # Ô nhập thông tin
        self.email_input = QLineEdit()
        self.new_username_input = QLineEdit()
        self.new_password_input = QLineEdit()

        self.email_input.setPlaceholderText("Email")
        self.new_username_input.setPlaceholderText("Tên đăng nhập")
        self.new_password_input.setPlaceholderText("Mật khẩu")
        self.new_password_input.setEchoMode(QLineEdit.Password)

        layout.addWidget(self.email_input)
        layout.addWidget(self.new_username_input)
        layout.addWidget(self.new_password_input)

        # Nút đăng ký
        register_btn = QPushButton("Đăng ký")
        register_btn.setStyleSheet("background-color: red; color: white; padding: 10px; min-width: 200px;")
        register_btn.clicked.connect(self.handleRegister)
        layout.addWidget(register_btn, alignment=Qt.AlignCenter)

        register_widget.setLayout(layout)
        self.setCentralWidget(register_widget)
        self.current_page = register_widget

    def handleRegister(self):
        email = self.email_input.text().strip()
        new_username = self.new_username_input.text().strip()
        new_password = self.new_password_input.text().strip()

        if not email or not new_username or not new_password:
            QMessageBox.warning(self, "Lỗi đăng ký", "Vui lòng nhập đầy đủ thông tin!")
            return

        if not self.is_valid_email(email):
            QMessageBox.warning(self, "Lỗi đăng ký", "Email không đúng định dạng! (phải có @gmail.com)")
            return

        if new_username in self.users_db:
            QMessageBox.warning(self, "Lỗi đăng ký", "Tên đăng nhập đã tồn tại! Hãy chọn tên khác.")
            return

        self.users_db[new_username] = {"password": new_password, "email": email}

        # Lưu thông tin người dùng vào file JSON
        self.save_users()

        QMessageBox.information(self, "Thành công", "Đăng ký thành công! Vui lòng đăng nhập.")
        self.showLoginPage()

    def is_valid_email(self, email):
        email_regex = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
        return re.match(email_regex, email) is not None

    def save_users(self):
        with open("users.json", "w") as f:
            json.dump(self.users_db, f)

    def load_users(self):
        try:
            with open("users.json", "r") as f:
                self.users_db = json.load(f)
        except FileNotFoundError:
            self.users_db = {}

    def showMainPage(self, username):
        if self.current_page:
            self.current_page.deleteLater()

        dashboard = QWidget()
        main_layout = QVBoxLayout(dashboard)

        # Header
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_label = QLabel("Hệ thống quản lý nông nghiệp")
        header_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        header_layout.addWidget(header_label)

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

        weather_icon = QLabel("☀️")
        weather_text = QLabel("Nắng")

        weather_icon.setStyleSheet("font-size: 48px;")
        weather_text.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")

        status_layout.addWidget(weather_icon, alignment=Qt.AlignCenter)
        status_layout.addWidget(weather_text, alignment=Qt.AlignCenter)

        # Thông số thời tiết
        params_widget = QWidget()
        params_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        params_grid = QGridLayout(params_widget)
        params_grid.setSpacing(15)

        params = [
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

        for i, (icon, label, value, unit) in enumerate(params):
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

    def updateDateTime(self):
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
            0: "Chủ Nhật"  # Thay đổi key 7 thành 0
        }
        
        # Sử dụng phương thức dayOfWeek() và lấy số dư khi chia cho 7
        weekday = current.date().dayOfWeek() % 7
        date_str = f"{day_map[weekday]}, {current.toString('dd-MM-yyyy')}"
        self.date_label.setText(date_str)

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