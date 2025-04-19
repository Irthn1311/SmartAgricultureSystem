from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QRegion

class LoginPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Tiêu đề
        app_name = QLabel(self.parent.get_translated_text('system_title'))
        app_name.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(app_name, alignment=Qt.AlignCenter)

        # Ô nhập
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.username_input.setPlaceholderText(self.parent.get_translated_text('username'))
        self.password_input.setPlaceholderText(self.parent.get_translated_text('password'))
        self.password_input.setEchoMode(QLineEdit.Password)

        show_password_cb = QCheckBox(self.parent.get_translated_text('show_password'))
        show_password_cb.stateChanged.connect(self.togglePasswordVisibility)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(show_password_cb)

        # Nút đăng nhập
        login_btn = QPushButton(self.parent.get_translated_text('login'))
        login_btn.setStyleSheet("background-color: #4a90e2; color: white; padding: 10px; min-width: 200px;")
        login_btn.clicked.connect(self.handleLogin)
        layout.addWidget(login_btn, alignment=Qt.AlignCenter)

        # Label hiển thị thông báo
        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message_label)

        self.setLayout(layout)

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

        if username not in self.parent.users_db or self.parent.users_db[username]["password"] != password:
            self.message_label.setText("Tên đăng nhập hoặc mật khẩu không đúng!")
            self.message_label.setStyleSheet("color: red;")
            return

        self.parent.current_user = username
        self.message_label.setText("Đăng nhập thành công!")
        self.message_label.setStyleSheet("color: green;")
        QTimer.singleShot(1000, lambda: self.parent.showMainPage(username))

    def show(self):
        self.parent.setCentralWidget(self) 