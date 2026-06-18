from models import database
from views.main_window import MainWindow
from controllers.budget_controller import BudgetController
from controllers.dashboard_controller import DashboardController
from controllers.analytics_controller import AnalyticsController
from controllers.ai_assistant_controller import AssistantController


class LoginController:
    def __init__(self, view):
        self.view = view

        # connect login button
        self.view.login_button.clicked.connect(self.login)
        self.view.register_button.clicked.connect(self.register)

    def login(self):
        username = self.view.username_input.text()
        password = self.view.password_input.text()

        # validation
        if not username or not password:
            self.view.show_message("Please fill in all fields")
            return

        # check user
        user = database.check_user(username, password)

        if user:
            self.view.show_message(
                "Login successful",
                success=True
            )

            # open main app
            self.main_window = MainWindow()

            self.main_window.settings_page.set_user(
                user["username"]
            )

            self.dashboard_controller = DashboardController(
                self.main_window.dashboard_page,
                user
            )

            self.analytics_controller = AnalyticsController(
                self.main_window.analytics_page,
                user
            )

            # AI assistant controller
            self.main_window.assistant_controller = (
                AssistantController(
                    self.main_window.assistant_page,
                    user
                )
            )

            # connect controller
            self.controller = BudgetController(
                self.main_window.transactions_page,
                user,
                self.main_window,
                self.dashboard_controller,
                self.analytics_controller
            )

            # show app
            self.main_window.show()

            # close login window
            self.view.close()

        else:
            self.view.show_message(
                "Incorrect username or password"
            )

    def register(self):
        username = self.view.username_input.text().strip()
        password = self.view.password_input.text().strip()

        if not username or not password:
            self.view.show_message("Please fill in all fields")
            return

        if len(username) < 3:
            self.view.show_message(
                "Username must contain at least 3 characters")
            return

        if len(password) < 4:
            self.view.show_message(
                "Password must contain at least 4 characters")
            return

        if database.username_exists(username):
            self.view.show_message("This username already exists")
            return

        database.create_user(username, password)

        self.view.show_message(
            "Account created successfully. You can now sign in.",
            success=True
        )

        self.view.password_input.clear()
