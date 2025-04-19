from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QButtonGroup, QFileDialog, QSizePolicy, QGridLayout, QFrame,
    QMessageBox, QGroupBox, QFormLayout, QSpinBox, QTimeEdit, QComboBox, QScrollArea
)
from PyQt5.QtCore import Qt, QTimer, QDateTime, QTime
from PyQt5.QtGui import QPixmap, QRegion

class WateringPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.current_widget = None
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.initUI()

    def initUI(self):
        # Xóa tất cả widget hiện có
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Content widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)

        # Tiêu đề
        title = QLabel(self.parent.get_translated_text('watering_options'))
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            margin: 20px 0;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 10px;
            text-align: center;
        """)
        self.content_layout.addWidget(title, alignment=Qt.AlignCenter)

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
                padding: 20px;
                min-width: 250px;
                min-height: 250px;
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
        manual_icon.setStyleSheet("font-size: 64px;")
        manual_text = QLabel(self.parent.get_translated_text('manual_watering'))
        manual_text.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color:rgb(0, 47, 255);
        """)
        manual_desc = QLabel(self.parent.get_translated_text('manual_watering_desc'))
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
                border-radius: 15px;
                padding: 20px;
                min-width: 250px;
                min-height: 250px;
            }
            QPushButton:hover {
                background-color: #FF6B6B;
            }
            QPushButton:hover QLabel {
                color: white;
            }
        """)
        auto_layout = QVBoxLayout(auto_btn)
        
        auto_icon = QLabel("⚙️")
        auto_icon.setStyleSheet("font-size: 64px;")
        auto_text = QLabel(self.parent.get_translated_text('auto_watering'))
        auto_text.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color:rgb(81, 255, 0);
        """)
        auto_desc = QLabel(self.parent.get_translated_text('auto_watering_desc'))
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
        self.content_layout.addWidget(buttons_container)

        # Kết nối sự kiện
        manual_btn.clicked.connect(self.showManualWatering)
        auto_btn.clicked.connect(self.showAutoWatering)

        self.content_layout.addStretch()

        # Navigation bar
        self.nav_bar = QWidget()
        self.nav_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        nav_layout = QHBoxLayout(self.nav_bar)
        nav_layout.setSpacing(10)

        nav_buttons = [
            ("🏠", self.parent.get_translated_text('home'), lambda: self.parent.showMainPage(self.parent.current_user)),
            ("🌤", self.parent.get_translated_text('weather'), self.parent.showWeatherDetails),
            ("💧", self.parent.get_translated_text('watering'), self.parent.showWateringOptions),
            ("⚙️", self.parent.get_translated_text('settings'), lambda: self.parent.showSettingsPage(self.parent.current_user))
        ]

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        for icon, tooltip, callback in nav_buttons:
            btn = QPushButton(icon)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setCheckable(True)
            btn.setToolTip(tooltip)
            if tooltip == self.parent.get_translated_text('watering'):
                btn.setChecked(True)
            btn.clicked.connect(callback)
            nav_layout.addWidget(btn)
            self.button_group.addButton(btn)

        self.nav_bar.setStyleSheet("""
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

        self.main_layout.addWidget(self.content_widget)
        self.main_layout.addWidget(self.nav_bar)

    def showManualWatering(self):
        # Xóa tất cả widget hiện có
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        manual_widget = QWidget()
        layout = QVBoxLayout(manual_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Tiêu đề
        title = QLabel(self.parent.get_translated_text('manual_watering'))
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
        
        self.manual_status_icon = QLabel("🔴" if not self.parent.manual_watering_on else "🟢")
        self.manual_status_icon.setStyleSheet("font-size: 48px;")
        
        self.manual_status_text = QLabel(
            self.parent.get_translated_text('system_on') if self.parent.manual_watering_on 
            else self.parent.get_translated_text('system_off')
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
        
        on_btn = QPushButton(f"🚿 {self.parent.get_translated_text('on')}")
        off_btn = QPushButton(f"💧 {self.parent.get_translated_text('off')}")

        for btn in [on_btn, off_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 20px;
                    padding: 20px;
                    min-width: 200px;
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
        back_btn = QPushButton(f"↩️ {self.parent.get_translated_text('back')}")
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
        back_btn.clicked.connect(self.showMainOptions)

        layout.addStretch()

        # Thêm navigation bar
        self.addNavigationBar(layout, self.parent.get_translated_text('watering'))

        # Thêm widget vào main layout
        self.main_layout.addWidget(manual_widget)

    def showAutoWatering(self):
        # Xóa tất cả widget hiện có
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

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
        title = QLabel(self.parent.get_translated_text('auto_watering_title'))
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
        
        self.auto_status_icon = QLabel("🔴" if not self.parent.auto_watering_on else "🟢")
        self.auto_status_icon.setStyleSheet("font-size: 64px;")
        
        status_text = self.parent.get_translated_text('auto_system_on' if self.parent.auto_watering_on else 'auto_system_off')
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
        settings_group = QGroupBox(self.parent.get_translated_text('auto_watering_settings'))
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
        start_label = QLabel(self.parent.get_translated_text('start_time_label'))
        start_label.setStyleSheet(label_style)
        self.start_time = QTimeEdit()
        self.start_time.setTime(QTime(6, 0))
        self.start_time.setDisplayFormat("HH:mm")
        self.start_time.setStyleSheet(control_style)

        # Thời gian kết thúc
        end_label = QLabel(self.parent.get_translated_text('end_time_label'))
        end_label.setStyleSheet(label_style)
        self.end_time = QTimeEdit()
        self.end_time.setTime(QTime(18, 0))
        self.end_time.setDisplayFormat("HH:mm")
        self.end_time.setStyleSheet(control_style)

        # Chu kỳ tưới
        cycle_label = QLabel(self.parent.get_translated_text('cycle_label'))
        cycle_label.setStyleSheet(label_style)
        self.cycle_combo = QComboBox()
        cycles = ['cycle_30min', 'cycle_1hour', 'cycle_2hours', 'cycle_4hours']
        self.cycle_combo.addItems([self.parent.get_translated_text(cycle) for cycle in cycles])
        self.cycle_combo.setStyleSheet(control_style)

        # Thời gian mỗi lần tưới
        duration_label = QLabel(self.parent.get_translated_text('duration_label'))
        duration_label.setStyleSheet(label_style)
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(1, 30)
        self.duration_spin.setValue(5)
        self.duration_spin.setSuffix(f" {self.parent.get_translated_text('minutes')}")
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
        back_btn = QPushButton(self.parent.get_translated_text('back_btn'))
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

        enable_btn = QPushButton(self.parent.get_translated_text('activate_btn'))
        disable_btn = QPushButton(self.parent.get_translated_text('deactivate_btn'))

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
        back_btn.clicked.connect(self.showMainOptions)
        enable_btn.clicked.connect(self.enable_auto_watering)
        disable_btn.clicked.connect(self.disable_auto_watering)

        # Thêm navigation bar
        self.addNavigationBar(layout, self.parent.get_translated_text('watering'))

        # Thêm widget vào main layout
        self.main_layout.addWidget(auto_widget)

    def showMainOptions(self):
        self.initUI()

    def turn_on_water(self):
        self.parent.manual_watering_on = True
        self.manual_status_icon.setText("🟢")
        self.manual_status_text.setText(self.parent.get_translated_text('system_on'))
        self.manual_status_text.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50;
            padding: 20px;
            background-color: #f8f8f8;
            border-radius: 15px;
        """)

    def turn_off_water(self):
        self.parent.manual_watering_on = False
        self.manual_status_icon.setText("🔴")
        self.manual_status_text.setText(self.parent.get_translated_text('system_off'))
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
            self.parent.auto_watering_on = True
            # Lưu các cài đặt hiện tại
            self.parent.auto_watering_settings = {
                'start_time': self.start_time.time().toString('HH:mm'),
                'end_time': self.end_time.time().toString('HH:mm'),
                'cycle': self.cycle_combo.currentText(),
                'duration': self.duration_spin.value()
            }
            
            self.auto_status_icon.setText("🟢")
            self.auto_status_text.setText(self.parent.get_translated_text('auto_system_on'))
            self.auto_status_text.setStyleSheet("""
                font-size: 24px;
                font-weight: bold;
                color: #4CAF50;
                padding: 20px;
                background-color: #f8f8f8;
                border-radius: 15px;
            """)
            
            settings_text = f"""
{self.parent.get_translated_text('operating_time')} {self.parent.auto_watering_settings['start_time']} - {self.parent.auto_watering_settings['end_time']}
{self.parent.get_translated_text('watering_cycle')} {self.parent.auto_watering_settings['cycle']}
{self.parent.get_translated_text('watering_duration')} {self.parent.auto_watering_settings['duration']} {self.parent.get_translated_text('minutes')}
            """
            self.settings_info.setText(settings_text)
            self.settings_info.show()
        except Exception as e:
            print(f"Lỗi trong enable_auto_watering: {str(e)}")

    def disable_auto_watering(self):
        try:
            self.parent.auto_watering_on = False
            self.parent.auto_watering_settings = None
            
            self.auto_status_icon.setText("🔴")
            self.auto_status_text.setText(self.parent.get_translated_text('auto_system_off'))
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
        nav_bar = QWidget()
        nav_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setSpacing(10)

        nav_buttons = [
            ("🏠", self.parent.get_translated_text('home'), lambda: self.parent.showMainPage(self.parent.current_user)),
            ("🌤", self.parent.get_translated_text('weather'), self.parent.showWeatherDetails),
            ("💧", self.parent.get_translated_text('watering'), self.parent.showWateringOptions),
            ("⚙️", self.parent.get_translated_text('settings'), lambda: self.parent.showSettingsPage(self.parent.current_user))
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

    def show(self):
        super().show()
        self.showMainOptions() 