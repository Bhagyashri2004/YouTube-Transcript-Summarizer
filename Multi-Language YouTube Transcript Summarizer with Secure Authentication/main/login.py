import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QLabel, QMessageBox
)
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QFont, QIcon
from PyQt6.QtCore import Qt
from database import init_db, register_user, login_user
from app import AppWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Login")
        self.resize(800, 500)
        self.setup_ui()

    def setup_ui(self):
        self.setAutoFillBackground(True)
        palette = QPalette()
        pixmap = QPixmap("background.jpg").scaled(
            self.width(), self.height(),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QWidget()
        card.setFixedSize(350, 320)
        card.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 0.5);
                border-radius: 20px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 20, 30, 20)

        title = QLabel("User Login")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: white; margin-bottom: 10px;")
        card_layout.addWidget(title)

        email_label = QLabel("User Name")
        email_label.setStyleSheet("color: white;")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter Username")
        self.email_input.setStyleSheet(self.input_style())
        card_layout.addWidget(email_label)
        card_layout.addWidget(self.email_input)

        password_label = QLabel("Password")
        password_label.setStyleSheet("color: white;")
        card_layout.addWidget(password_label)

        password_layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(self.input_style())

        self.eye_button = QPushButton()
        self.eye_button.setIcon(QIcon("eye_close.png"))
        self.eye_button.setCheckable(True)
        self.eye_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.eye_button.setStyleSheet("QPushButton { border: none; background-color: transparent; }")
        self.eye_button.setFixedSize(30, 30)
        self.eye_button.clicked.connect(self.toggle_password_visibility)

        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.eye_button)

        password_widget = QWidget()
        password_widget.setLayout(password_layout)
        card_layout.addWidget(password_widget)

        self.submit_button = QPushButton("Login")
        self.submit_button.setStyleSheet(self.button_style())
        self.submit_button.clicked.connect(self.handle_login)
        card_layout.addWidget(self.submit_button)

        self.register_button = QPushButton("Register")
        self.register_button.setStyleSheet("color: white; background-color: transparent; border: none;")
        self.register_button.clicked.connect(self.show_register)
        card_layout.addWidget(self.register_button, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(card)
        self.setLayout(main_layout)

    def input_style(self):
        return """
            QLineEdit {
                padding: 8px;
                border-radius: 6px;
                background-color: rgba(255, 255, 255, 0.7);
                border: none;
                color: black;
            }
            QLineEdit::placeholder {
                color: #555555;
            }
        """


    def button_style(self):
        return """
            QPushButton {
                background-color: #5A00B0;
                color: white;
                font-weight: bold;
                border: none;
                padding: 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #7D2DE0;
            }
        """

    def toggle_password_visibility(self):
        if self.eye_button.isChecked():
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.eye_button.setIcon(QIcon("eye_open.png"))
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.eye_button.setIcon(QIcon("eye_close.png"))

    def handle_login(self):
        username = self.email_input.text().strip()
        password = self.password_input.text().strip()
        if login_user(username, password):
            self.hide()
            self.app_window = AppWindow()
            self.app_window.show()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid credentials.")

    def show_register(self):
        self.hide()
        self.register_window = RegistrationWindow(self)
        self.register_window.show()

    def resizeEvent(self, event):
        pixmap = QPixmap("background.jpg").scaled(
            self.width(), self.height(),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        palette = self.palette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)
        super().resizeEvent(event)


class RegistrationWindow(QWidget):
    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window
        self.setWindowTitle("Register")
        self.resize(800, 500)
        self.setup_ui()

    def setup_ui(self):
        self.setAutoFillBackground(True)
        palette = QPalette()
        pixmap = QPixmap("background.jpg").scaled(
            self.width(), self.height(),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QWidget()
        card.setFixedSize(350, 360)
        card.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 0.5);
                border-radius: 20px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 20, 30, 20)

        title = QLabel("Register")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: white; margin-bottom: 10px;")
        card_layout.addWidget(title)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("User Name")
        self.email_input.setStyleSheet(self.input_style())
        card_layout.addWidget(self.email_input)

        # Password with toggle
        password_layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(self.input_style())
        self.eye_button_pass = QPushButton()
        self.eye_button_pass.setIcon(QIcon("eye_close.png"))
        self.eye_button_pass.setCheckable(True)
        self.eye_button_pass.setCursor(Qt.CursorShape.PointingHandCursor)
        self.eye_button_pass.setStyleSheet("QPushButton { border: none; background-color: transparent; }")
        self.eye_button_pass.setFixedSize(30, 30)
        self.eye_button_pass.clicked.connect(self.toggle_password_visibility)
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.eye_button_pass)
        password_widget = QWidget()
        password_widget.setLayout(password_layout)
        card_layout.addWidget(password_widget)

        # Confirm password with toggle
        confirm_layout = QHBoxLayout()
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirm Password")
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_input.setStyleSheet(self.input_style())
        self.eye_button_confirm = QPushButton()
        self.eye_button_confirm.setIcon(QIcon("eye_close.png"))
        self.eye_button_confirm.setCheckable(True)
        self.eye_button_confirm.setCursor(Qt.CursorShape.PointingHandCursor)
        self.eye_button_confirm.setStyleSheet("QPushButton { border: none; background-color: transparent; }")
        self.eye_button_confirm.setFixedSize(30, 30)
        self.eye_button_confirm.clicked.connect(self.toggle_confirm_visibility)
        confirm_layout.addWidget(self.confirm_input)
        confirm_layout.addWidget(self.eye_button_confirm)
        confirm_widget = QWidget()
        confirm_widget.setLayout(confirm_layout)
        card_layout.addWidget(confirm_widget)

        register_button = QPushButton("Register")
        register_button.setStyleSheet(self.button_style())
        register_button.clicked.connect(self.handle_register)
        card_layout.addWidget(register_button)

        back_button = QPushButton("Back to Login")
        back_button.setStyleSheet("color: white; background-color: transparent; border: none;")
        back_button.clicked.connect(self.show_login)
        card_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(card)
        self.setLayout(main_layout)

    def toggle_password_visibility(self):
        if self.eye_button_pass.isChecked():
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.eye_button_pass.setIcon(QIcon("eye_open.png"))
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.eye_button_pass.setIcon(QIcon("eye_close.png"))

    def toggle_confirm_visibility(self):
        if self.eye_button_confirm.isChecked():
            self.confirm_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.eye_button_confirm.setIcon(QIcon("eye_open.png"))
        else:
            self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.eye_button_confirm.setIcon(QIcon("eye_close.png"))

    def input_style(self):
        return """
            QLineEdit {
                padding: 8px;
                border-radius: 6px;
                background-color: rgba(255, 255, 255, 0.7);
                border: none;
                color: black;
            }
            QLineEdit::placeholder {
                color: #555555;
            }
        """

    def button_style(self):
        return """
            QPushButton {
                background-color: #5A00B0;
                color: white;
                font-weight: bold;
                border: none;
                padding: 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #7D2DE0;
            }
        """

    def handle_register(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        confirm = self.confirm_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        if password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        if register_user(email, password):
            QMessageBox.information(self, "Success", "Registration successful. Please log in.")
            self.close()
            self.login_window.show()
        else:
            QMessageBox.warning(self, "Error", "User already exists.")

    def show_login(self):
        self.close()
        self.login_window.show()

    def resizeEvent(self, event):
        pixmap = QPixmap("background.jpg").scaled(
            self.width(), self.height(),
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        palette = self.palette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)
        super().resizeEvent(event)

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
