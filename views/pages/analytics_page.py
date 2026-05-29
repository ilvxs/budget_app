from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QGridLayout,
    QTextEdit,
    QGraphicsDropShadowEffect,
    QSizePolicy,
    QScrollArea
)

from PySide6.QtGui import QColor

from PySide6.QtCharts import (
    QChart,
    QChartView,
    QLineSeries,
    QValueAxis,
    QCategoryAxis
)

from PySide6.QtCore import Qt


class AnalyticsPage(QWidget):

    def __init__(self):
        super().__init__()

        # =========================
        # MAIN LAYOUT
        # =========================

        outer_layout = QVBoxLayout(self)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        outer_layout.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)

        self.main_layout = QVBoxLayout(container)

        self.main_layout.setContentsMargins(25, 25, 25, 25)
        self.main_layout.setSpacing(25)

        # =========================
        # TITLE
        # =========================

        title = QLabel("📊 Analytics")

        title.setStyleSheet("""
        font-size: 28px;
        font-weight: bold;
        color: #1e293b;
        """)

        self.main_layout.addWidget(title)

        # =========================
        # EVOLUTION CHART
        # =========================

        self.chart = QChart()

        self.chart.setTitle("Spending Evolution")

        self.chart_view = QChartView(self.chart)

        self.chart_view.setMinimumHeight(350)

        self.chart_view.setStyleSheet("""
        background-color: white;
        border-radius: 18px;
        padding: 10px;
        """)

        self.main_layout.addWidget(self.chart_view)

        # =========================
        # AI INSIGHTS TITLE
        # =========================

        insights_title = QLabel("🧠 AI Insights")

        insights_title.setStyleSheet("""
        font-size: 22px;
        font-weight: bold;
        color: #1e293b;
        """)

        self.main_layout.addWidget(insights_title)

        # =========================
        # INSIGHTS GRID
        # =========================

        self.insights_widget = QWidget()

        self.insights_layout = QGridLayout()

        self.insights_layout.setSpacing(20)

        self.insights_widget.setLayout(
            self.insights_layout
        )

        self.main_layout.addWidget(
            self.insights_widget
        )

        # cards
        self.card1 = self.create_card("")
        self.card2 = self.create_card("")
        self.card3 = self.create_card("")
        self.card4 = self.create_card("")

        self.insights_layout.addWidget(self.card1, 0, 0)
        self.insights_layout.addWidget(self.card2, 0, 1)
        self.insights_layout.addWidget(self.card3, 1, 0)
        self.insights_layout.addWidget(self.card4, 1, 1)

        self.insights_layout.setColumnStretch(0, 1)
        self.insights_layout.setColumnStretch(1, 1)

        # =========================
        # ANOMALY TITLE
        # =========================

        anomaly_title = QLabel("⚠️ Anomaly Detection")

        anomaly_title.setStyleSheet("""
        font-size: 22px;
        font-weight: bold;
        color: #1e293b;
        """)

        self.main_layout.addWidget(anomaly_title)

        # =========================
        # ANOMALY BOX
        # =========================

        self.anomaly_box = QTextEdit()
        self.anomaly_box.setStyleSheet("""
            background-color: white;
            color: #1e293b;
            border-radius: 18px;
            padding: 15px;
            font-size: 15px;
        """)

        self.anomaly_box.setReadOnly(True)

        self.anomaly_box.setMinimumHeight(150)

        self.anomaly_box.setText(
            "No anomalies detected."
        )

        self.main_layout.addWidget(self.anomaly_box)

        # =========================
        # STYLE
        # =========================

        self.setStyleSheet("""
        QWidget {
            background-color: #f5f7fa;
            font-family: Segoe UI;
        }

        QTextEdit {
            background-color: white;
            border-radius: 18px;
            padding: 15px;
            font-size: 15px;
            color: #1e293b;
            selection-background-color: #3b82f6;
        }
        """)

    # ==================================
    # CREATE CARD
    # ==================================

    def create_card(self, text):

        card = QFrame()

        card.setMinimumHeight(170)

        card.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

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

        layout = QVBoxLayout()

        layout.setContentsMargins(20, 20, 20, 20)

        card.setLayout(layout)

        label = QLabel(text)

        label.setWordWrap(True)

        label.setStyleSheet("""
        font-size: 16px;
        font-weight: bold;
        color: #334155;
        """)

        layout.addWidget(label)

        card.label = label

        return card

    # ==================================
    # UPDATE CHART
    # ==================================

    def update_chart(self, months, values):

        self.chart.removeAllSeries()

        for axis in self.chart.axes():
            self.chart.removeAxis(axis)

        series = QLineSeries()

        for i, value in enumerate(values):
            series.append(i, value)

        self.chart.addSeries(series)

        axis_x = QCategoryAxis()
        axis_x.setTitleText("Month")

        for i, month in enumerate(months):
            axis_x.append(month, i)

        axis_x.setRange(0, max(len(months) - 1, 1))

        axis_y = QValueAxis()
        axis_y.setTitleText("Expenses")

        if values:
            axis_y.setRange(0, max(values) + 500)
        else:
            axis_y.setRange(0, 100)

        self.chart.addAxis(axis_x, Qt.AlignBottom)
        self.chart.addAxis(axis_y, Qt.AlignLeft)

        series.attachAxis(axis_x)
        series.attachAxis(axis_y)

    # ==================================
    # UPDATE INSIGHTS
    # ==================================

    def update_insights(self, insights):

        cards = [
            self.card1,
            self.card2,
            self.card3,
            self.card4
        ]

        for card, text in zip(cards, insights):

            card.label.setText(text)
