from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QGraphicsDropShadowEffect,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)

from PySide6.QtGui import QColor

from PySide6.QtCore import Qt

from PySide6.QtCharts import (
    QChart,
    QChartView,
    QPieSeries,
    QBarSeries,
    QBarSet,
    QBarCategoryAxis,
    QValueAxis
)


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        # MAIN LAYOUT

        self.main_layout = QVBoxLayout()

        self.main_layout.setContentsMargins(25, 25, 25, 25)
        self.main_layout.setSpacing(20)

        self.setLayout(self.main_layout)

        # TITLE

        title = QLabel("📊 Dashboard")

        title.setStyleSheet("""
        font-size: 28px;
        font-weight: bold;
        color: #1e293b;
        """)

        self.main_layout.addWidget(title)

        # CARDS LAYOUT

        from PySide6.QtWidgets import QGridLayout
        cards_layout = QGridLayout()
        cards_layout.setHorizontalSpacing(20)
        cards_layout.setVerticalSpacing(20)

        cards_layout.setSpacing(20)

        self.main_layout.addLayout(cards_layout)

        # CARDS

        self.revenues_card = self.create_card(
            "💰 Revenues",
            "0 MAD",
            "#22c55e"
        )

        self.expenses_card = self.create_card(
            "💸 Expenses",
            "0 MAD",
            "#ef4444"
        )

        self.balance_card = self.create_card(
            "📈 Balance",
            "0 MAD",
            "#3b82f6"
        )

        self.transactions_card = self.create_card(
            "🧾 Transactions",
            "0",
            "#a855f7"
        )

        cards_layout.addWidget(self.revenues_card, 0, 0)
        cards_layout.addWidget(self.expenses_card, 0, 1)
        cards_layout.addWidget(self.balance_card, 1, 0)
        cards_layout.addWidget(self.transactions_card, 1, 1)

        # CHARTS LAYOUT

        charts_layout = QHBoxLayout()

        charts_layout.setSpacing(20)

        self.main_layout.addLayout(charts_layout)

        # MONTHLY CHART

        self.monthly_chart = QChart()
        self.monthly_chart.setTitle("Monthly Overview")

        self.monthly_chart_view = QChartView(self.monthly_chart)

        self.monthly_chart_view.setMinimumHeight(350)

        charts_layout.addWidget(self.monthly_chart_view)

        # PIE CHART

        self.pie_chart = QChart()
        self.pie_chart.setTitle("Expense Categories")

        self.pie_chart_view = QChartView(self.pie_chart)

        self.pie_chart_view.setMinimumHeight(350)

        charts_layout.addWidget(self.pie_chart_view)

        # STYLE

        self.setStyleSheet("""
        QWidget {
            background-color: #f5f7fa;
            font-family: Segoe UI;
        }
        """)

    # CREATE CARD

    def create_card(self, title, value, color):

        card = QFrame()

        card.setMinimumHeight(170)

        card.setStyleSheet(f"""
        QFrame {{
            background-color: white;
            border-left: 8px solid {color};
            border-radius: 18px;
        }}
        """)

        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(6)

        shadow.setColor(QColor(0, 0, 0, 40))

        card.setGraphicsEffect(shadow)

        layout = QVBoxLayout()

        layout.setContentsMargins(20, 20, 20, 20)

        card.setLayout(layout)

        title_label = QLabel(title)

        title_label.setStyleSheet("""
        font-size: 16px;
        font-weight: bold;
        color: #64748b;
        """)

        value_label = QLabel(value)

        value_label.setStyleSheet(f"""
        font-size: 30px;
        font-weight: bold;
        color: {color};
        """)

        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(value_label)

        # save value label
        card.value_label = value_label

        return card

    def update_cards(self, revenues, expenses, transactions):

        revenues = revenues or 0
        expenses = expenses or 0

        balance = revenues - expenses

        self.revenues_card.value_label.setText(f"{revenues} MAD")

        self.expenses_card.value_label.setText(f"{expenses} MAD")

        self.balance_card.value_label.setText(f"{balance} MAD")

        self.transactions_card.value_label.setText(
            str(transactions)
        )

    def update_monthly_chart(self, revenues, expenses):

        self.monthly_chart.removeAllSeries()

        for axis in self.monthly_chart.axes():
            self.monthly_chart.removeAxis(axis)

        revenues_set = QBarSet("Revenues")
        expenses_set = QBarSet("Expenses")

        revenues_set.append(revenues)
        expenses_set.append(expenses)

        series = QBarSeries()

        series.append(revenues_set)
        series.append(expenses_set)

        self.monthly_chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append(["Budget"])

        axis_y = QValueAxis()

        self.monthly_chart.addAxis(axis_x, Qt.AlignBottom)
        self.monthly_chart.addAxis(axis_y, Qt.AlignLeft)

        series.attachAxis(axis_x)
        series.attachAxis(axis_y)

    def update_pie_chart(self, categories):

        self.pie_chart.removeAllSeries()

        for axis in self.pie_chart.axes():
            self.pie_chart.removeAxis(axis)
        series = QPieSeries()

        for category, total in categories:
            series.append(category, float(total))

        self.pie_chart.addSeries(series)
