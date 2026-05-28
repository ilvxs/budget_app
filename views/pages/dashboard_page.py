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

        # =========================
        # MAIN LAYOUT
        # =========================

        self.main_layout = QVBoxLayout()

        self.main_layout.setContentsMargins(25, 25, 25, 25)
        self.main_layout.setSpacing(20)

        self.setLayout(self.main_layout)

        # =========================
        # TITLE
        # =========================

        title = QLabel("📊 Dashboard")

        title.setStyleSheet("""
        font-size: 28px;
        font-weight: bold;
        color: #1e293b;
        """)

        self.main_layout.addWidget(title)

        # =========================
        # CARDS LAYOUT
        # =========================

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        self.main_layout.addLayout(cards_layout)

        # =========================
        # CARDS
        # =========================

        self.revenus_card = self.create_card(
            "💰 Revenus",
            "0 MAD",
            "#22c55e"
        )

        self.depenses_card = self.create_card(
            "💸 Dépenses",
            "0 MAD",
            "#ef4444"
        )

        self.solde_card = self.create_card(
            "📈 Solde",
            "0 MAD",
            "#3b82f6"
        )

        self.transactions_card = self.create_card(
            "🧾 Transactions",
            "0",
            "#a855f7"
        )

        cards_layout.addWidget(self.revenus_card)
        cards_layout.addWidget(self.depenses_card)
        cards_layout.addWidget(self.solde_card)
        cards_layout.addWidget(self.transactions_card)

        # =========================
        # CHARTS LAYOUT
        # =========================

        charts_layout = QHBoxLayout()

        charts_layout.setSpacing(20)

        self.main_layout.addLayout(charts_layout)

        # =========================
        # MONTHLY CHART
        # =========================

        self.monthly_chart = QChart()
        self.monthly_chart.setTitle("Monthly Overview")

        self.monthly_chart_view = QChartView(self.monthly_chart)

        self.monthly_chart_view.setMinimumHeight(350)

        charts_layout.addWidget(self.monthly_chart_view)

        # =========================
        # PIE CHART
        # =========================

        self.pie_chart = QChart()
        self.pie_chart.setTitle("Expense Categories")

        self.pie_chart_view = QChartView(self.pie_chart)

        self.pie_chart_view.setMinimumHeight(350)

        charts_layout.addWidget(self.pie_chart_view)

        # =========================
        # STYLE
        # =========================

        self.setStyleSheet("""
        QWidget {
            background-color: #f5f7fa;
            font-family: Segoe UI;
        }
        """)

    # ==================================
    # CREATE CARD
    # ==================================

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

    def update_cards(self, revenus, depenses, transactions):

        revenus = revenus or 0
        depenses = depenses or 0

        solde = revenus - depenses

        self.revenus_card.value_label.setText(f"{revenus} MAD")

        self.depenses_card.value_label.setText(f"{depenses} MAD")

        self.solde_card.value_label.setText(f"{solde} MAD")

        self.transactions_card.value_label.setText(
            str(transactions)
        )

    def update_monthly_chart(self, revenus, depenses):

        self.monthly_chart.removeAllSeries()

        for axis in self.monthly_chart.axes():
            self.monthly_chart.removeAxis(axis)

        revenues_set = QBarSet("Revenus")
        depenses_set = QBarSet("Dépenses")

        revenues_set.append(revenus)
        depenses_set.append(depenses)

        series = QBarSeries()

        series.append(revenues_set)
        series.append(depenses_set)

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
