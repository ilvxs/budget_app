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

        high_expenses = database.get_high_expenses(
            self.user["id"]
        )

        messages = []

        for category, montant, date in high_expenses:

            if montant >= 2000:

                messages.append(
                    f"⚠️ High expense detected: "
                    f"{montant} MAD in {category} ({date})"
                )

        self.view.anomaly_box.setText(
            "\n\n".join(messages)
        )

        # Spending spike detection
        current_expenses = database.get_current_month_expenses(
            self.user["id"]
        )

        previous_expenses = database.get_previous_month_expenses(
            self.user["id"]
        )

        if previous_expenses > 0:

            increase = (
                (current_expenses - previous_expenses)
                / previous_expenses
            ) * 100

            if increase > 40:

                messages.append(
                    f"⚠️ Expenses increased by "
                    f"{increase:.1f}% compared to last month."
                )

        # Category abuse detection
        categories = database.get_current_month_categories(
            self.user["id"]
        )

        for category, current_total in categories:

            current_total = float(current_total)

            average = float(
                database.get_category_average(
                    self.user["id"],
                    category)
            )

            if average > 0:

                threshold = average + (average * 0.5)

                if current_total > threshold:

                    increase_percent = (
                        (current_total - average) / average
                    ) * 100

                    messages.append(
                        f"⚠️ Category anomaly detected: {category}\n"
                        f"This month's spending: {current_total:.2f} MAD\n"
                        f"Previous monthly average: {average:.2f} MAD\n"
                        f"Increase: {increase_percent:.1f}% above normal"
                    )
        if not messages:
            messages.append(
                "✅ No anomalies detected."
            )

        self.view.anomaly_box.setText(
            "\n\n".join(messages)
        )
