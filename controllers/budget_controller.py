from models import database
import matplotlib.pyplot as plt
from openpyxl import Workbook
from PySide6.QtWidgets import QMessageBox


class BudgetController:
    def __init__(self, view, user, main_window, dashboard_controller, analytics_controller):
        self.view = view
        self.user = user
        self.main_window = main_window
        self.dashboard_controller = dashboard_controller
        self.analytics_controller = analytics_controller

        # connect buttons
        self.view.add_button.clicked.connect(self.add_transaction)
        self.view.delete_button.clicked.connect(
            self.delete_selected_transaction)
        self.view.filter_button.clicked.connect(self.filter_transactions)
        self.view.chart_button.clicked.connect(self.show_chart)
        self.view.export_button.clicked.connect(self.export_excel)
        self.main_window.logout_button.clicked.connect(self.logout)

        # load data at startup
        self.load_transactions()

    def update_totals(self):
        # get selected values directly
        month = self.view.month_filter.currentText()
        year = self.view.year_filter.currentText()
        category = self.view.category_filter.currentText()

        revenues, expenses = database.get_totals(
            self.user["id"],
            month,
            year,
            category
        )
        self.view.update_totals(revenues, expenses)

    def add_transaction(self):
        amount = self.view.amount_input.text()
        type_ = self.view.type_input.currentText()
        category = self.view.category_input.currentText()
        description = self.view.description_input.text()
        date = self.view.date_input.date().toString("yyyy-MM-dd")

        # message + validation
        if not amount:
            self.view.show_message("Amount is required")
            return

        try:
            amount = float(amount)
        except:
            self.view.show_message("Invalid amount")
            return

        database.insert_transaction(
            type_,
            amount,
            category,
            description,
            date,
            self.user["id"]
        )

        # clear fields, show message, and reload data
        self.view.clear_inputs()
        self.view.show_message("Transaction added ✅")
        self.load_transactions()
        self.dashboard_controller.load_dashboard()
        self.analytics_controller.load_analytics()

        self.dashboard_controller.load_dashboard()

    def load_transactions(self):
        # Instead of loading all data, apply the current filter directly.
        # This keeps the table and totals synchronized with the dropdown filters.
        self.filter_transactions()
        # REFRESH DASHBOARD AUTOMATICALLY
        self.update_dashboard()

    def delete_selected_transaction(self):
        selected = self.view.table.currentRow()

        if selected == -1:
            self.view.show_message("Select a transaction")
            return

        # column 1 = real ID
        id_item = self.view.table.item(selected, 1)

        if id_item is None:
            return

        id_ = int(id_item.text())

        confirmation = self.view.confirm_delete()

        if confirmation == QMessageBox.Yes:
            database.delete_transaction(id_)

            self.load_transactions()
            self.dashboard_controller.load_dashboard()
            self.analytics_controller.load_analytics()

            self.dashboard_controller.load_dashboard()

            self.view.show_message("Transaction deleted 🔴")

    def filter_transactions(self):
        month = self.view.month_filter.currentText()
        year = self.view.year_filter.currentText()
        category = self.view.category_filter.currentText()

        data = database.get_transactions_filtered(
            self.user["id"], month, year, category)
        self.view.update_table(data)

        self.update_totals()

    # display a chart
    def show_chart(self):
        month = self.view.month_filter.currentText()
        year = self.view.year_filter.currentText()
        category = self.view.category_filter.currentText()

        revenues, expenses = database.get_totals(
            self.user["id"],
            month,
            year,
            category
        )

        # Clean values by replacing None with 0
        clean_revenues = revenues or 0
        clean_expenses = expenses or 0

        # Validation: if both values are 0, cancel display
        if clean_revenues == 0 and clean_expenses == 0:
            self.view.show_message(
                "No data to display for this period.")
            return

        labels = ['Revenues', 'Expenses']
        values = [clean_revenues, clean_expenses]

        # Clear the previous figure to avoid overlapping charts
        plt.clf()

        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title("Budget Breakdown")
        plt.show()

    # export data to Excel
    def export_excel(self):
        data = database.get_all_transactions(
            self.user["id"]
        )

        wb = Workbook()
        ws = wb.active

        ws.append(["ID", "Type", "Amount", "Category", "Description", "Date"])

        for row in data:
            ws.append(row)

        wb.save("transactions.xlsx")

        self.view.show_message("Excel export successful 💾")

    def logout(self):
        reply = QMessageBox.question(
            self.view,
            "Logout",
            "Do you really want to log out?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:

            # local imports to avoid circular import
            from views.login_window import LoginWindow
            from controllers.login_controller import LoginController

            # open login
            self.login_window = LoginWindow()

            self.login_controller = LoginController(
                self.login_window
            )

            self.login_window.show()

            # close dashboard
            self.main_window.close()

    def update_dashboard(self):
        revenues, expenses, transactions = database.get_dashboard_data(
            self.user["id"]
        )

        self.main_window.dashboard_page.update_cards(
            revenues,
            expenses,
            transactions
        )
