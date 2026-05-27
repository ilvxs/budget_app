import sys

from PySide6.QtWidgets import QApplication

from views.login_window import LoginWindow
from controllers.login_controller import LoginController


app = QApplication(sys.argv)

# login window
login_window = LoginWindow()

# controller
controller = LoginController(login_window)

login_window.show()

sys.exit(app.exec())
