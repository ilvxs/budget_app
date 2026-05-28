from models import database


class AnalyticsController:

    def __init__(self, view, user):

        self.view = view
        self.user = user

        self.load_analytics()

    def load_analytics(self):

        # =========================
        # CHART
        # =========================

        data = database.get_monthly_expenses(
            self.user["id"]
        )

        values = []

        for row in data:
            values.append(float(row[1]))

        self.view.update_chart(values)

        # =========================
        # INSIGHTS
        # =========================

        insights = []

        # biggest category
        biggest = database.get_biggest_expense_category(
            self.user["id"]
        )

        if biggest:
            insights.append(
                f"Biggest expense: {biggest[0]}"
            )
        else:
            insights.append(
                "No expenses yet."
            )

        # monthly average
        avg = database.get_average_monthly_expense(
            self.user["id"]
        )

        insights.append(
            f"📈 Average monthly expense: {round(avg, 2)} MAD"
        )

        # spending evolution
        current = database.get_current_month_expenses(
            self.user["id"]
        )

        previous = database.get_previous_month_expenses(
            self.user["id"]
        )

        if previous > 0:

            change = ((current - previous) / previous) * 100

            if change > 0:
                insights.append(
                    f"⚠️ Expenses increased by {round(change, 1)}%"
                )
            else:
                insights.append(
                    f"✅ Expenses decreased by {abs(round(change, 1))}%"
                )

        else:
            insights.append(
                "📊 Not enough data for comparison."
            )

        # savings
        revenues = database.get_current_month_revenues(
            self.user["id"]
        )

        expenses = database.get_current_month_expenses(
            self.user["id"]
        )

        estimated_savings = revenues - expenses

        insights.append(
            f"💰 Estimated savings for this month: {round(estimated_savings, 2)} MAD"
        )

        self.view.update_insights(insights)
