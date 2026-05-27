from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton
)

from PySide6.QtCore import Qt


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Window
        self.setWindowTitle("Login")
        self.resize(400, 300)

        # Layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(20)

        self.setLayout(self.layout)

        # Title
        title = QLabel("🔐 Connexion")
        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #1e293b;
        """)

        self.layout.addWidget(title)

        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur")

        self.layout.addWidget(self.username_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")

        # Hide password
        self.password_input.setEchoMode(QLineEdit.Password)

        self.layout.addWidget(self.password_input)

        # Login button
        self.login_button = QPushButton("🔓 Se connecter")

        self.layout.addWidget(self.login_button)

        # Message label
        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.message_label)

        # Style
        self.setStyleSheet("""
        QWidget {
            background-color: #f5f7fa;
            font-family: Segoe UI;
            font-size: 14px;
        }

        QLineEdit {
            padding: 10px;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            background-color: white;
            color: #111827;
        }

        QPushButton {
            background-color: #2563eb;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #1d4ed8;
        }

        QLabel {
            color: #374151;
        }
        """)

        # Cursor
        self.login_button.setCursor(Qt.PointingHandCursor)

    def show_message(self, text, success=False):
        if success:
            color = "#16a34a"
        else:
            color = "#dc2626"

        self.message_label.setStyleSheet(f"""
            color: {color};
            font-weight: bold;
        """)

        self.message_label.setText(text)
