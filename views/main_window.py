from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
    QStackedWidget
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

# pages
from views.pages.transactions_page import TransactionsPage
from views.pages.dashboard_page import DashboardPage
from views.pages.analytics_page import AnalyticsPage
from views.pages.ai_assistant_page import AssistantPage
from views.pages.settings_page import SettingsPage


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        # =========================
        # WINDOW
        # =========================

        self.setWindowTitle("Budget AI")
        self.resize(1400, 850)

        # =========================
        # MAIN LAYOUT
        # =========================

        self.main_layout = QHBoxLayout()

        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.setLayout(self.main_layout)

        # =========================
        # SIDEBAR
        # =========================

        self.sidebar = QFrame()

        self.sidebar.setFixedWidth(240)

        self.sidebar.setStyleSheet("""
        background-color: #1e293b;
        """)

        self.sidebar_layout = QVBoxLayout()

        self.sidebar_layout.setContentsMargins(15, 20, 15, 20)
        self.sidebar_layout.setSpacing(12)

        self.sidebar.setLayout(self.sidebar_layout)

        # =========================
        # TITLE
        # =========================

        title = QLabel("💰 Budget AI")

        title.setStyleSheet("""
        color: white;
        font-size: 26px;
        font-weight: bold;
        padding: 10px;
        """)

        self.sidebar_layout.addWidget(title)

        # =========================
        # SIDEBAR BUTTON STYLE
        # =========================

        self.sidebar_button_style = """
        QPushButton {
            background-color: transparent;
            color: white;
            text-align: left;
            padding: 14px;
            border-radius: 10px;
            font-size: 15px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #334155;
        }
        """

        # =========================
        # BUTTONS
        # =========================

        self.dashboard_button = QPushButton("🏠 Dashboard")
        self.transactions_button = QPushButton("💳 Transactions")
        self.analytics_button = QPushButton("📊 Analytics")
        self.assistant_button = QPushButton("🤖 AI Assistant")
        self.settings_button = QPushButton("⚙️ Settings")

        self.sidebar_buttons = [
            self.dashboard_button,
            self.transactions_button,
            self.analytics_button,
            self.assistant_button,
            self.settings_button
        ]

        for btn in self.sidebar_buttons:
            btn.setStyleSheet(self.sidebar_button_style)
            btn.setCursor(Qt.PointingHandCursor)

            self.sidebar_layout.addWidget(btn)

        self.sidebar_layout.addStretch()

        # =========================
        # LOGOUT
        # =========================

        self.logout_button = QPushButton("🚪 Logout")

        self.logout_button.setStyleSheet(self.sidebar_button_style)

        self.logout_button.setCursor(Qt.PointingHandCursor)

        self.sidebar_layout.addWidget(self.logout_button)

        # =========================
        # STACKED WIDGET
        # =========================

        self.pages = QStackedWidget()

        # pages
        self.dashboard_page = DashboardPage()
        self.transactions_page = TransactionsPage()
        self.analytics_page = AnalyticsPage()
        self.assistant_page = AssistantPage()
        self.settings_page = SettingsPage()

        # add pages
        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.transactions_page)
        self.pages.addWidget(self.analytics_page)
        self.pages.addWidget(self.assistant_page)
        self.pages.addWidget(self.settings_page)

        # =========================
        # ADD TO MAIN LAYOUT
        # =========================

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.pages)

        # =========================
        # NAVIGATION
        # =========================

        self.dashboard_button.clicked.connect(
            lambda: self.pages.setCurrentWidget(
                self.dashboard_page
            )
        )

        self.transactions_button.clicked.connect(
            lambda: self.pages.setCurrentWidget(
                self.transactions_page
            )
        )

        self.analytics_button.clicked.connect(
            lambda: self.pages.setCurrentWidget(
                self.analytics_page
            )
        )

        self.assistant_button.clicked.connect(
            lambda: self.pages.setCurrentWidget(
                self.assistant_page
            )
        )

        self.settings_button.clicked.connect(
            lambda: self.pages.setCurrentWidget(
                self.settings_page
            )
        )

        # default page
        self.pages.setCurrentWidget(
            self.transactions_page
        )
