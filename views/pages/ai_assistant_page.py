from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QLabel,
    QHBoxLayout
)

from PySide6.QtCore import Qt


class AssistantPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title = QLabel("🤖 AI Financial Assistant")

        title.setStyleSheet("""
        font-size: 28px;
        font-weight: bold;
        color: #1e293b;
        """)

        layout.addWidget(title)

        self.chat_box = QTextEdit()

        self.chat_box.setReadOnly(True)

        self.chat_box.setMinimumHeight(520)

        layout.addWidget(self.chat_box)

        input_layout = QHBoxLayout()

        self.input = QLineEdit()

        self.input.setPlaceholderText(
            "Ask something about your finances..."
        )

        self.send_button = QPushButton("Send")

        self.send_button.setCursor(Qt.PointingHandCursor)

        input_layout.addWidget(self.input)
        input_layout.addWidget(self.send_button)

        layout.addLayout(input_layout)

        self.setLayout(layout)

        self.setStyleSheet("""
        QWidget {
            background-color: #f5f7fa;
            font-family: Segoe UI;
        }

        QLabel {
            color: #1e293b;
        }

        QTextEdit {
            background-color: white;
            color: #0f172a;
            border-radius: 18px;
            padding: 14px;
            font-size: 14px;
            border: none;
        }

        QLineEdit {
            background-color: white;
            color: #0f172a;
            border-radius: 12px;
            padding: 12px;
            font-size: 14px;
            border: 1px solid #cbd5e1;
        }

        QPushButton {
            background-color: #3b82f6;
            color: white;
            border-radius: 12px;
            padding: 10px 22px;
            font-size: 14px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #2563eb;
        }
        """)
