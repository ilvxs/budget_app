from models import database
from views.main_window import MainWindow
from controllers.budget_controller import BudgetController
from controllers.dashboard_controller import DashboardController


class LoginController:
    def __init__(self, view):
        self.view = view

        # connect login button
        self.view.login_button.clicked.connect(self.login)

    def login(self):
        username = self.view.username_input.text()
        password = self.view.password_input.text()

        # validation
        if not username or not password:
            self.view.show_message("Remplissez tous les champs")
            return

        # check user
        user = database.check_user(username, password)

        if user:
            self.view.show_message(
                "Connexion réussie ✅",
                success=True
            )

            # open main app
            self.main_window = MainWindow()

            # connect controller
            self.controller = BudgetController(
                self.main_window.transactions_page,
                user,
                self.main_window
            )

            self.main_window.dashboard_controller = DashboardController(
                self.main_window.dashboard_page,
                user
            )

            self.main_window.show()

            # close login window
            self.view.close()

        else:
            self.view.show_message(
                "Nom d'utilisateur ou mot de passe incorrect"
            )
