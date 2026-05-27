from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("⚙️ Settings")

        title.setStyleSheet("""
        font-size: 28px;
        font-weight: bold;
        """)

        layout.addWidget(title)

        self.setLayout(layout)
