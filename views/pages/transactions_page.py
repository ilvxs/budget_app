from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem,
    QLabel, QDateEdit, QMessageBox,
    QHeaderView, QGraphicsDropShadowEffect,
)
from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QColor


class TransactionsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        self.setLayout(self.main_layout)
        #  1. Inputs
        input_layout = QHBoxLayout()

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")

        self.type_input = QComboBox()
        self.type_input.addItems(["revenue", "expense"])

        self.category_input = QComboBox()
        self.category_input.addItems(
            ["Food", "Transport", "Housing", "Bills", "Leisure", "Other"])

        self.type_input.currentTextChanged.connect(self.update_categories)

        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Description")

        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        # self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.date_input.setCalendarPopup(True)

        # --- ADD button (standard green) ---
        self.add_button = QPushButton("➕ Add")
        self.add_button.setStyleSheet("background-color: #4CAF50;")
        self.add_button.setCursor(Qt.PointingHandCursor)

        input_layout.addWidget(self.amount_input)
        input_layout.addWidget(self.type_input)
        input_layout.addWidget(self.category_input)
        input_layout.addWidget(self.description_input)
        input_layout.addWidget(self.date_input)
        input_layout.addWidget(self.add_button)

        self.main_layout.addLayout(input_layout)

        #  2. Filter
        filter_layout = QHBoxLayout()

        self.month_filter = QComboBox()
        self.month_filter.addItem("All")
        self.month_filter.addItems([str(i) for i in range(1, 13)])

        self.year_filter = QComboBox()
        self.year_filter.addItem("All")
        self.year_filter.addItems(["2025", "2026", "2027"])

        # Select today's date by default
        current_date = QDate.currentDate()
        self.month_filter.setCurrentText(str(current_date.month()))
        self.year_filter.setCurrentText(str(current_date.year()))

        self.category_filter = QComboBox()
        self.category_filter.addItem("All")
        self.category_filter.addItems(
            ["Food", "Transport", "Housing", "Bills", "Leisure", "Salary", "Freelance", "Other"])

        self.filter_button = QPushButton("Filter")
        self.filter_button.setStyleSheet("background-color: #b104e5;")
        self.filter_button.setCursor(Qt.PointingHandCursor)

        filter_layout.addWidget(self.month_filter)
        filter_layout.addWidget(self.year_filter)
        filter_layout.addWidget(self.category_filter)
        filter_layout.addWidget(self.filter_button)

        self.main_layout.addLayout(filter_layout)

        #  3. Table
        self.table = QTableWidget()
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "N°", "ID", "Type", "Amount", "Category", "Description", "Date"
        ])

        self.main_layout.addWidget(self.table)

        self.table.verticalHeader().setDefaultSectionSize(40)

        #  4. Totals
        self.total_revenues_label = QLabel("Total revenues: 0")
        self.total_expenses_label = QLabel("Total expenses: 0")
        self.balance_label = QLabel("Balance: 0")

        totals_layout = QHBoxLayout()

        self.total_revenues_label.setStyleSheet("""
        background-color: #dcfce7;
        padding: 15px;
        border-radius: 10px;
        color: #166534;
        """)

        self.total_expenses_label.setStyleSheet("""
        background-color: #fee2e2;
        padding: 15px;
        border-radius: 10px;
        color: #991b1b;
        """)

        self.balance_label.setStyleSheet("""
        background-color: #dbeafe;
        padding: 15px;
        border-radius: 10px;
        color: #1e40af;
        """)

        totals_layout.addWidget(self.total_revenues_label)
        totals_layout.addWidget(self.total_expenses_label)
        totals_layout.addWidget(self.balance_label)

        self.main_layout.addLayout(totals_layout)

        #  5. DELETE button (red)
        self.delete_button = QPushButton("🗑️ Delete")
        self.delete_button.setStyleSheet("background-color: #f44336;")
        self.delete_button.setCursor(Qt.PointingHandCursor)
        self.main_layout.addWidget(self.delete_button)

        #  6. CHART button (blue)
        self.chart_button = QPushButton("📊 Show Chart")
        self.chart_button.setStyleSheet("background-color: #2196F3;")
        self.chart_button.setCursor(Qt.PointingHandCursor)
        self.main_layout.addWidget(self.chart_button)

        #  7. Excel EXPORT button
        self.export_button = QPushButton("💾 Export Excel")
        self.export_button.setStyleSheet("background-color: #1B5E20;")
        self.export_button.setCursor(Qt.PointingHandCursor)
        self.main_layout.addWidget(self.export_button)

        self.update_categories()
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f7fa;
                font-family: Segoe UI;
                font-size: 14px;
            }

            QLineEdit, QComboBox, QDateEdit {
                padding: 8px;
                min-height: 20px;
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

            QTableWidget {
                background-color: white;
                border-radius: 10px;
                gridline-color: #e5e7eb;
                color: #111827;
                selection-background-color: #2563eb;
                selection-color: white;
            }

            QHeaderView::section {
                background-color: #2563eb;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }

            QComboBox QAbstractItemView {
                background-color: white;
                color: #111827;
                selection-background-color: #2563eb;
                selection-color: white;
                border-radius: 8px;
                padding: 5px;
            }
            QLabel {
                color: #374151;
                font-weight: bold;
            }
            QCalendarWidget QWidget {
                background-color: white;
                color: #111827;
            }

            QCalendarWidget QToolButton {
                background-color: #eb2563;
                color: #111827;
                border: none;
                padding: 5px;
                padding-left: 10px;
                padding-right: 10px;
                border-radius: 2px;
            }

            QCalendarWidget QMenu {
                background-color: white;
                color: #111827;
            }

            QCalendarWidget QSpinBox {
                background-color: white;
                color: #111827;
                border: 1px solid #d1d5db;
                border-radius: 5px;
                padding: 2px;
            }

            QCalendarWidget QAbstractItemView {
                selection-background-color: #2563eb;
                selection-color: white;
                background-color: white;
                color: #111827;
            }
            """)

        self.add_shadow(self.table)

        self.add_shadow(self.add_button)
        self.add_shadow(self.filter_button)
        self.add_shadow(self.delete_button)
        self.add_shadow(self.chart_button)
        self.add_shadow(self.export_button)

        self.add_shadow(self.total_revenues_label)
        self.add_shadow(self.total_expenses_label)
        self.add_shadow(self.balance_label)

    def update_categories(self):
        type_ = self.type_input.currentText()

        self.category_input.clear()

        if type_ == "revenue":
            self.category_input.addItems(["Salary", "Freelance", "Other"])
        else:
            self.category_input.addItems(
                ["Food", "Transport", "Housing", "Bills", "Leisure", "Other"])

    def update_table(self, data):
        self.table.setRowCount(0)
        self.table.setColumnCount(7)

        for row_number, row_data in enumerate(data):
            self.table.insertRow(row_number)

            # display number (1,2,3...)
            self.table.setItem(
                row_number, 0, QTableWidgetItem(str(row_number + 1)))

            for column_number, value in enumerate(row_data):
                self.table.setItem(
                    row_number,
                    column_number + 1,  # +1 because the first column is for the display number
                    QTableWidgetItem(str(value))
                )

    def update_totals(self, revenues, expenses):
        revenues = revenues or 0
        expenses = expenses or 0

        balance = revenues - expenses

        self.total_revenues_label.setText(f"Total revenues: {revenues}")
        self.total_expenses_label.setText(f"Total expenses: {expenses}")
        self.balance_label.setText(f"Balance: {balance}")

    def show_message(self, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.exec()

    def clear_inputs(self):
        self.amount_input.clear()
        self.description_input.clear()
        self.date_input.setDate(QDate.currentDate())

    def add_shadow(self, widget):
        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)

        shadow.setColor(QColor(0, 0, 0, 60))

        widget.setGraphicsEffect(shadow)

    def confirm_delete(self):
        msg = QMessageBox()

        msg.setWindowTitle("Confirmation")
        msg.setText("Do you really want to delete this transaction?")

        msg.setIcon(QMessageBox.Warning)

        msg.setStandardButtons(
            QMessageBox.Yes | QMessageBox.No
        )

        msg.setDefaultButton(QMessageBox.No)

        return msg.exec()
