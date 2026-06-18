from models import database


class DashboardController:

    def __init__(self, view, user):

        self.view = view
        self.user = user

        self.load_dashboard()

    def load_dashboard(self):

        # TOTALS

        revenues, expenses = database.get_totals(
            self.user["id"],
            "All",
            "All",
            "All"
        )

        # TRANSACTIONS COUNT

        data = database.get_all_transactions(
            self.user["id"]
        )

        transactions_count = len(data)

        self.view.update_cards(
            revenues,
            expenses,
            transactions_count
        )

        # MONTHLY CHART

        self.view.update_monthly_chart(
            revenues or 0,
            expenses or 0
        )

        # PIE CHART

        categories = database.get_expenses_by_category(
            self.user["id"]
        )

        self.view.update_pie_chart(categories)
