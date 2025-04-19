from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QButtonGroup, QFileDialog, QSizePolicy, QGridLayout, QFrame,
    QMessageBox, QGroupBox, QFormLayout, QSpinBox, QTimeEdit, QComboBox, QScrollArea,
    QDialog, QLineEdit
)
from PyQt5.QtCore import Qt, QTimer, QDateTime, QTime
from PyQt5.QtGui import QPixmap, QRegion

class SettingsPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.current_page = None  # Thêm thuộc tính current_page
        # Thêm danh sách ngôn ngữ
        self.languages = {
            "vi": "Tiếng Việt",
            "en": "English",
            "auto": "Tự động theo hệ thống"
        }
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        # Tiêu đề
        title = QLabel(self.parent.get_translated_text('settings'))
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

        # Các nút chức năng
        buttons_widget = QWidget()
        buttons_layout = QVBoxLayout(buttons_widget)
        buttons_layout.setSpacing(20)

        # Nút thông tin cá nhân
        personal_info_btn = QPushButton(f"👤 {self.parent.get_translated_text('personal_info')}")
        personal_info_btn.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                padding: 20px;
                background-color: #4a90e2;
                color: white;
                border-radius: 15px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
        """)
        personal_info_btn.clicked.connect(lambda: self.showUserInfoDialog(self.parent.current_user))

        # Nút ngôn ngữ
        language_btn = QPushButton(f"🌐 {self.parent.get_translated_text('language')}")
        language_btn.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                padding: 20px;
                background-color: #4a90e2;
                color: white;
                border-radius: 15px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
        """)
        language_btn.clicked.connect(self.showLanguagePage)

        buttons_layout.addWidget(personal_info_btn)
        buttons_layout.addWidget(language_btn)
        content_layout.addWidget(buttons_widget)

        content_layout.addStretch()

        # Navigation bar
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
            if tooltip == self.parent.get_translated_text('settings'):
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

        layout.addWidget(content_widget)
        layout.addWidget(nav_bar)

    def showUserInfoDialog(self, username):
        dialog = QDialog(self)
        dialog.setWindowTitle(self.parent.get_translated_text('personal_info'))
        dialog.setModal(True)
        dialog.setMinimumWidth(400)

        layout = QVBoxLayout(dialog)

        form_layout = QFormLayout()
        form_layout.setSpacing(20)

        # Username
        username_label = QLabel(self.parent.get_translated_text('username'))
        username_value = QLabel(username)
        form_layout.addRow(username_label, username_value)

        # Email
        email_label = QLabel(self.parent.get_translated_text('email'))
        email_input = QLineEdit()
        email_input.setText(self.parent.users_db[username]["email"])
        form_layout.addRow(email_label, email_input)

        # Current password
        current_password_label = QLabel(self.parent.get_translated_text('current_password'))
        current_password_input = QLineEdit()
        current_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow(current_password_label, current_password_input)

        # New password
        new_password_label = QLabel(self.parent.get_translated_text('new_password'))
        new_password_input = QLineEdit()
        new_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow(new_password_label, new_password_input)

        # Confirm new password
        confirm_password_label = QLabel(self.parent.get_translated_text('confirm_password'))
        confirm_password_input = QLineEdit()
        confirm_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow(confirm_password_label, confirm_password_input)

        layout.addLayout(form_layout)

        # Buttons
        buttons_layout = QHBoxLayout()
        save_btn = QPushButton(self.parent.get_translated_text('save'))
        cancel_btn = QPushButton(self.parent.get_translated_text('cancel'))

        for btn in [save_btn, cancel_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    padding: 10px 20px;
                    border-radius: 5px;
                    font-weight: bold;
                }
            """)

        save_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        cancel_btn.setStyleSheet("background-color: #f44336; color: white;")

        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addLayout(buttons_layout)

        # Kết nối sự kiện
        save_btn.clicked.connect(lambda: self.saveUserSettings(username, dialog, email_input, current_password_input, new_password_input, confirm_password_input))
        cancel_btn.clicked.connect(dialog.reject)

        dialog.exec_()

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
        title = QLabel(self.parent.get_translated_text('select_language'))
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
            
            if lang == self.parent.current_language:
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
        back_btn = QPushButton("↩️ " + self.parent.get_translated_text('back'))
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
        back_btn.clicked.connect(lambda: self.parent.showSettingsPage(self.parent.current_user))
        content_layout.addWidget(back_btn, alignment=Qt.AlignCenter)

        # Thêm content widget vào main layout
        main_layout.addWidget(content_widget)

        # Navigation bar
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
            if tooltip == self.parent.get_translated_text('settings'):
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

        self.setLayout(main_layout)
        self.current_page = language_widget

    def saveUserSettings(self, username, dialog, email_input, current_password_input, new_password_input, confirm_password_input):
        email = email_input.text().strip()
        current_password = current_password_input.text()
        new_password = new_password_input.text()
        confirm_password = confirm_password_input.text()

        # Kiểm tra email
        if not self.isValidEmail(email):
            QMessageBox.warning(dialog, self.parent.get_translated_text('error'), self.parent.get_translated_text('invalid_email'))
            return

        # Nếu có thay đổi mật khẩu
        if current_password or new_password or confirm_password:
            if current_password != self.parent.users_db[username]["password"]:
                QMessageBox.warning(dialog, self.parent.get_translated_text('error'), self.parent.get_translated_text('wrong_password'))
                return

            if new_password != confirm_password:
                QMessageBox.warning(dialog, self.parent.get_translated_text('error'), self.parent.get_translated_text('password_mismatch'))
                return

            if len(new_password) < 4:
                QMessageBox.warning(dialog, self.parent.get_translated_text('error'), self.parent.get_translated_text('password_length'))
                return

            self.parent.users_db[username]["password"] = new_password

        # Cập nhật email
        self.parent.users_db[username]["email"] = email

        QMessageBox.information(dialog, self.parent.get_translated_text('success'), self.parent.get_translated_text('update_success'))
        dialog.accept()

    def isValidEmail(self, email):
        return '@' in email and '.' in email

    def changeLanguage(self, lang):
        try:
            # Cập nhật ngôn ngữ hiện tại
            self.parent.current_language = lang
            
            # Xác định trang hiện tại
            current_page = None
            if hasattr(self.parent, 'button_group') and self.parent.button_group:
                checked_button = self.parent.button_group.checkedButton()
                if checked_button:
                    current_page = checked_button.toolTip()

            # Cập nhật giao diện với ngôn ngữ mới
            if self.parent.current_user:
                # Tải lại trang hiện tại với ngôn ngữ mới
                if current_page == self.parent.get_translated_text('home'):
                    self.parent.showMainPage(self.parent.current_user)
                elif current_page == self.parent.get_translated_text('weather'):
                    self.parent.showWeatherDetails()
                elif current_page == self.parent.get_translated_text('watering'):
                    self.parent.showWateringOptions()
                elif current_page == self.parent.get_translated_text('settings'):
                    self.parent.showSettingsPage(self.parent.current_user)
                else:
                    # Mặc định quay về trang cài đặt
                    self.parent.showSettingsPage(self.parent.current_user)
            else:
                # Nếu chưa đăng nhập, cập nhật trang đăng nhập
                self.parent.showLoginPage()

            # Hiển thị thông báo
            QMessageBox.information(
                self,
                self.parent.get_translated_text('success'),
                f"{self.parent.get_translated_text('language_changed')} {self.languages[lang]}"
            )

        except Exception as e:
            print(f"Lỗi khi thay đổi ngôn ngữ: {str(e)}")
            QMessageBox.critical(
                self,
                self.parent.get_translated_text('error'),
                f"Đã xảy ra lỗi khi thay đổi ngôn ngữ: {str(e)}"
            )

    def show(self, username):
        self.parent.setCentralWidget(self) 