from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class AnalyticsPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("📊 Analytics")

        title.setStyleSheet("""
        font-size: 28px;
        font-weight: bold;
        """)

        layout.addWidget(title)

        self.setLayout(layout)
