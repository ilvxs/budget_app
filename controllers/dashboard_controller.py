from models import database


class DashboardController:

    def __init__(self, view, user):

        self.view = view
        self.user = user

        self.load_dashboard()

    def load_dashboard(self):

        # =========================
        # TOTALS
        # =========================

        revenus, depenses = database.get_totaux(
            self.user["id"],
            "Tous",
            "Tous",
            "Toutes"
        )

        # =========================
        # TRANSACTIONS COUNT
        # =========================

        data = database.get_all_transactions(
            self.user["id"]
        )

        transactions_count = len(data)

        self.view.update_cards(
            revenus,
            depenses,
            transactions_count
        )

        # =========================
        # MONTHLY CHART
        # =========================

        self.view.update_monthly_chart(
            revenus or 0,
            depenses or 0
        )

        # =========================
        # PIE CHART
        # =========================

        categories = database.get_expenses_by_category(
            self.user["id"]
        )

        self.view.update_pie_chart(categories)
