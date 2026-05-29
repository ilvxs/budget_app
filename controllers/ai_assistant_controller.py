from services.gemini_service import ask_ai
from models import database

import html
import re


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
            {transactions[-8:]}
        """

        return context

    def send_message(self):

        question = self.view.input.text().strip()

        if not question:
            return

        self.view.chat_box.append(
            f"""
            <div style="
                background-color:#dbeafe;
                color:#1e3a8a;
                padding:10px;
                border-radius:10px;
                margin-bottom:8px;
            ">
                <b>You:</b> {html.escape(question)}
            </div>
            """
        )

        financial_context = self.build_financial_context()

        full_prompt = f"""
            You are an AI financial assistant inside a personal budget management app.

            You must only answer questions related to:
            - personal finance
            - expenses
            - revenues
            - budget management
            - savings
            - spending analysis
            - anomalies
            - financial recommendations

            If the user asks something unrelated, politely say:
            "I'm designed to help only with your budget and financial data."

            Use ONLY the financial data below.
            Do not invent transactions or numbers.
            Give practical advice.
            Keep the answer clear and professional.

            {financial_context}

            USER QUESTION:
            {question}
        """

        try:
            response = ask_ai(full_prompt)

            formatted_response = self.format_ai_response(response)

            self.view.chat_box.append(
                f"""
                    <div style="
                        background-color:#f8fafc;
                        color:#0f172a;
                        padding:12px;
                        border-radius:10px;
                        margin-bottom:12px;
                        line-height:1.5;
                    ">
                        <b>AI:</b><br>{formatted_response}
                    </div>
                """
            )

        except Exception as e:
            error_text = str(e)

            if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                self.view.chat_box.append(
                    """
                    <div style="color:#dc2626;">
                        <b>AI:</b> Gemini quota is temporarily unavailable. Please try again later.
                    </div>
                    """
                )
            elif "API key" in error_text or "401" in error_text:
                self.view.chat_box.append(
                    """
                    <div style="color:#dc2626;">
                        <b>AI:</b> API key problem. Check your Gemini API key.
                    </div>
                    """
                )
            else:
                self.view.chat_box.append(
                    f"""
                    <div style="color:#dc2626;">
                        <b>ERROR:</b> {html.escape(error_text)}
                    </div>
                    """
                )

        self.view.input.clear()

    def format_ai_response(self, text):
        # Escape unsafe HTML first
        text = html.escape(text)

        # Convert markdown bold **text** to HTML bold
        text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)

        # Convert line breaks
        text = text.replace("\n", "<br>")

        return text
