from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QButtonGroup, QFileDialog, QSizePolicy, QGridLayout, QFrame
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QPixmap, QRegion

class MainPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

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
        self.user_image_label.mousePressEvent = lambda event: self.uploadImage()
        self.user_image_label.setText("Chọn ảnh")
        self.user_image_label.setStyleSheet("border: 1px dashed #ccc; padding: 10px;")

        # Tạo mặt nạ hình tròn
        mask = QRegion(0, 0, 50, 50, QRegion.Ellipse)
        self.user_image_label.setMask(mask)

        user_info_layout.addWidget(self.user_image_label)

        # Username Label
        self.username_label = QLabel()
        self.username_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        user_info_layout.addWidget(self.username_label)

        header_layout.addWidget(user_info_widget)

        # Logout Button
        logout_btn = QPushButton(self.parent.get_translated_text('logout'))
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
        logout_btn.clicked.connect(self.parent.logout)
        header_layout.addWidget(logout_btn, alignment=Qt.AlignRight)

        # Time Widget
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

        # Weather Widget
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
            ("🌡", self.parent.get_translated_text('temperature'), "**", "°C"),
            ("💨", self.parent.get_translated_text('wind_speed'), "**", "km/h"),
            ("💧", self.parent.get_translated_text('humidity'), "**", "%"),
            ("🏗", self.parent.get_translated_text('precipitation'), "**", "%")
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
            ("🏠", self.parent.get_translated_text('home')),
            ("🌤", self.parent.get_translated_text('weather')),
            ("💧", self.parent.get_translated_text('watering')),
            ("⚙️", self.parent.get_translated_text('settings'))
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
        layout.addWidget(header_widget)
        layout.addWidget(time_widget)
        layout.addWidget(weather_widget)
        layout.addStretch()
        layout.addWidget(nav_bar)

        self.setStyleSheet("background-color: #f5f6fa;")

        # Cập nhật thời gian
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)

        # Set trang chủ là active
        self.button_group.buttons()[0].setChecked(True)

        # Kết nối sự kiện click vào các nút
        self.button_group.buttons()[1].clicked.connect(self.parent.showWeatherDetails)
        self.button_group.buttons()[2].clicked.connect(self.parent.showWateringOptions)
        self.button_group.buttons()[3].clicked.connect(lambda: self.parent.showSettingsPage(self.parent.current_user))

    def updateDateTime(self):
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
        weekday_text = self.parent.get_translated_text(weekday_map[weekday])
        
        # Format ngày tháng theo ngôn ngữ
        if self.parent.current_language == "en":
            date_str = f"{weekday_text}, {current.toString('MM-dd-yyyy')}"
        else:
            date_str = f"{weekday_text}, {current.toString('dd-MM-yyyy')}"

        self.date_label.setText(date_str)

    def uploadImage(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Chọn ảnh", "", "Image Files (*.png *.jpg *.jpeg)")

        if file_path and self.parent.current_user:
            self.parent.users_db[self.parent.current_user]["image"] = file_path
            user_image = QPixmap(file_path)
            self.user_image_label.setPixmap(user_image)

            # Cập nhật mặt nạ hình tròn sau khi tải ảnh mới
            mask = QRegion(0, 0, 50, 50, QRegion.Ellipse)
            self.user_image_label.setMask(mask)

    def show(self, username=None):
        if username:
            self.parent.current_user = username
            self.username_label.setText(username)
            
            # Cập nhật ảnh đại diện nếu có
            if "image" in self.parent.users_db[username]:
                user_image = QPixmap(self.parent.users_db[username]["image"])
                self.user_image_label.setPixmap(user_image)
            else:
                self.user_image_label.setText("Chọn ảnh")
                self.user_image_label.setStyleSheet("border: 1px dashed #ccc; padding: 10px;")
        
        self.parent.setCentralWidget(self) 