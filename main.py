import sys
from PySide6.QtWidgets import QApplication
from views.main_window import MainWindow
from controllers.budget_controller import BudgetController

app = QApplication(sys.argv)

window = MainWindow()
controller = BudgetController(window)

window.show()

sys.exit(app.exec())
