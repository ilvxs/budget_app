from services.openai_service import ask_ai
from models import database


class AssistantController:

    def __init__(self, view, user):

        self.view = view
        self.user = user

        self.view.send_button.clicked.connect(
            self.send_message
        )

    def build_financial_context(self):

        user_id = self.user["id"]

        revenues = database.get_current_month_revenues(
            user_id
        )

        expenses = database.get_current_month_expenses(
            user_id
        )

        biggest = database.get_biggest_expense_category(
            user_id
        )

        avg = database.get_average_monthly_expense(
            user_id
        )

        previous = database.get_previous_month_expenses(
            user_id
        )

        categories = database.get_expenses_by_category(
            user_id
        )

        transactions = database.get_all_transactions(
            user_id
        )

        context = f"""
            FINANCIAL DATA:

            Current month revenues: {revenues} MAD
            Current month expenses: {expenses} MAD

            Average monthly expenses: {avg} MAD

            Previous month expenses: {previous} MAD

            Biggest expense category:
            {biggest}

            Expenses by category:
            {categories}

            Recent transactions:
            {transactions[-15:]}
        """

        return context

    def send_message(self):

        question = self.view.input.text()

        if not question:
            return

        self.view.chat_box.append(
            f"<b>You:</b> {question}"
        )

        financial_context = (
            self.build_financial_context()
        )

        full_prompt = f"""
            {financial_context}

            USER QUESTION:
            {question}
        """

        try:

            response = ask_ai(full_prompt)

            self.view.chat_box.append(
                f"<b>AI:</b> {response}"
            )

        except Exception as e:

            self.view.chat_box.append(
                f"<b>ERROR:</b> {str(e)}"
            )

        self.view.input.clear()
