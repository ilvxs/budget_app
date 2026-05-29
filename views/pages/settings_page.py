from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QHBoxLayout,
    QPushButton,
    QGraphicsDropShadowEffect
)

from PySide6.QtGui import QColor
from PySide6.QtCore import Qt


class SettingsPage(QWidget):

    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.main_layout.setContentsMargins(25, 25, 25, 25)
        self.main_layout.setSpacing(20)

        self.setLayout(self.main_layout)

        title = QLabel("⚙️ Settings")

        title.setStyleSheet("""
        font-size: 28px;
        font-weight: bold;
        color: #1e293b;
        """)

        self.main_layout.addWidget(title)

        # Profile card
        self.profile_card = self.create_card()

        profile_layout = QVBoxLayout()
        self.profile_card.setLayout(profile_layout)

        profile_title = QLabel("👤 User Profile")
        profile_title.setStyleSheet("""
        font-size: 20px;
        font-weight: bold;
        color: #1e293b;
        """)

        self.username_label = QLabel("Username: -")
        self.username_label.setStyleSheet("""
        font-size: 16px;
        color: #334155;
        """)

        profile_layout.addWidget(profile_title)
        profile_layout.addWidget(self.username_label)

        self.main_layout.addWidget(self.profile_card)

        # App info card
        self.app_card = self.create_card()

        app_layout = QVBoxLayout()
        self.app_card.setLayout(app_layout)

        app_title = QLabel("💰 Application Info")
        app_title.setStyleSheet("""
        font-size: 20px;
        font-weight: bold;
        color: #1e293b;
        """)

        app_info = QLabel(
            "Budget AI is a personal finance desktop application "
            "with transactions management, dashboard charts, analytics, "
            "anomaly detection, and AI assistant."
        )

        app_info.setWordWrap(True)

        app_info.setStyleSheet("""
        font-size: 15px;
        color: #334155;
        """)

        app_layout.addWidget(app_title)
        app_layout.addWidget(app_info)

        self.main_layout.addWidget(self.app_card)

        # AI status card
        self.ai_card = self.create_card()

        ai_layout = QVBoxLayout()
        self.ai_card.setLayout(ai_layout)

        ai_title = QLabel("🤖 AI Assistant")
        ai_title.setStyleSheet("""
        font-size: 20px;
        font-weight: bold;
        color: #1e293b;
        """)

        ai_info = QLabel(
            "AI Provider: Gemini API\n"
            "Model: gemini-flash-lite-latest\n"
            "Status: Configured if API key is valid"
        )

        ai_info.setStyleSheet("""
        font-size: 15px;
        color: #334155;
        """)

        ai_layout.addWidget(ai_title)
        ai_layout.addWidget(ai_info)

        self.main_layout.addWidget(self.ai_card)

        # Future settings card
        self.future_card = self.create_card()

        future_layout = QVBoxLayout()
        self.future_card.setLayout(future_layout)

        future_title = QLabel("🔧 Future Options")
        future_title.setStyleSheet("""
        font-size: 20px;
        font-weight: bold;
        color: #1e293b;
        """)

        future_info = QLabel(
            "- Dark mode\n"
            "- Password update\n"
            "- Notifications\n"
            "- Currency preference\n"
            "- Register screen\n"
            "- More advanced prediction system\n"
            "- Budget goals\n"
            "- Better AI memory and conversation history"
        )

        future_info.setStyleSheet("""
        font-size: 15px;
        color: #334155;
        """)

        future_layout.addWidget(future_title)
        future_layout.addWidget(future_info)

        self.main_layout.addWidget(self.future_card)

        self.main_layout.addStretch()

        self.setStyleSheet("""
        QWidget {
            background-color: #f5f7fa;
            font-family: Segoe UI;
        }
        """)

    def create_card(self):

        card = QFrame()

        card.setStyleSheet("""
        QFrame {
            background-color: white;
            border-radius: 18px;
        }
        """)

        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(6)
        shadow.setColor(QColor(0, 0, 0, 40))

        card.setGraphicsEffect(shadow)

        return card

    def set_user(self, username):

        self.username_label.setText(
            f"Username: {username}"
        )
