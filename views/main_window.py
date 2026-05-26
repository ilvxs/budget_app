import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem,
    QLabel, QDateEdit, QMessageBox
)
from PySide6.QtCore import QDate


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Improve UI design: ajoute du style
        self.setStyleSheet("""
            QWidget {
                font-size: 14px;
            }
            QPushButton {
                color: white;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QLineEdit, QComboBox {
                padding: 5px;
            }
        """)

        #  Fenêtre
        self.setWindowTitle("Gestion de Budget")
        self.resize(900, 700)

        #  Layout principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        #  1. Inputs
        input_layout = QHBoxLayout()

        self.montant_input = QLineEdit()
        self.montant_input.setPlaceholderText("Montant")

        self.type_input = QComboBox()
        self.type_input.addItems(["revenu", "depense"])

        self.categorie_input = QComboBox()
        self.categorie_input.addItems(
            ["Food", "Transport", "Logement", "Factures", "Autre"])

        self.type_input.currentTextChanged.connect(self.update_categories)

        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Description")

        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        # self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.date_input.setCalendarPopup(True)

        # --- Bouton AJOUTER (Vert standard) ---
        self.add_button = QPushButton("Ajouter")
        self.add_button.setStyleSheet("background-color: #4CAF50;")

        input_layout.addWidget(self.montant_input)
        input_layout.addWidget(self.type_input)
        input_layout.addWidget(self.categorie_input)
        input_layout.addWidget(self.description_input)
        input_layout.addWidget(self.date_input)
        input_layout.addWidget(self.add_button)

        self.layout.addLayout(input_layout)

        #  2. Filtre
        filter_layout = QHBoxLayout()

        self.month_filter = QComboBox()
        self.month_filter.addItem("Tous")
        self.month_filter.addItems([str(i) for i in range(1, 13)])

        self.year_filter = QComboBox()
        self.year_filter.addItem("Tous")
        self.year_filter.addItems(["2025", "2026", "2027"])

        # Sélectionner la date d'aujourd'hui par défaut ---
        current_date = QDate.currentDate()
        self.month_filter.setCurrentText(str(current_date.month()))
        self.year_filter.setCurrentText(str(current_date.year()))

        self.category_filter = QComboBox()
        self.category_filter.addItem("Toutes")
        self.category_filter.addItems(
            ["Food", "Transport", "Logement", "Factures", "Salaire", "Freelance", "Autre"])

        self.filter_button = QPushButton("Filtrer")
        self.filter_button.setStyleSheet("background-color: #b104e5;")

        filter_layout.addWidget(self.month_filter)
        filter_layout.addWidget(self.year_filter)
        filter_layout.addWidget(self.category_filter)
        filter_layout.addWidget(self.filter_button)

        self.layout.addLayout(filter_layout)

        #  3. Tableau
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "N°", "ID", "Type", "Montant", "Catégorie", "Description", "Date"
        ])

        self.layout.addWidget(self.table)

        #  4. Totaux
        self.total_revenus_label = QLabel("Total revenus: 0")
        self.total_depenses_label = QLabel("Total dépenses: 0")
        self.solde_label = QLabel("Solde: 0")

        self.layout.addWidget(self.total_revenus_label)
        self.layout.addWidget(self.total_depenses_label)
        self.layout.addWidget(self.solde_label)

        #  5. Bouton SUPPRIMER (Rouge)
        self.delete_button = QPushButton("Supprimer")
        self.delete_button.setStyleSheet("background-color: #f44336;")
        self.layout.addWidget(self.delete_button)

        #  6. Bouton GRAPHIQUE (Bleu)
        self.chart_button = QPushButton("Afficher graphique")
        self.chart_button.setStyleSheet("background-color: #2196F3;")
        self.layout.addWidget(self.chart_button)

        #  7. Bouton EXPORT Excel
        self.export_button = QPushButton("Exporter Excel")
        self.export_button.setStyleSheet("background-color: #1B5E20;")
        self.layout.addWidget(self.export_button)

        self.update_categories()

    def confirm_delete(self):
        msg = QMessageBox()

        msg.setWindowTitle("Confirmation")
        msg.setText("Voulez-vous vraiment supprimer cette transaction ?")

        msg.setIcon(QMessageBox.Warning)

        msg.setStandardButtons(
            QMessageBox.Yes | QMessageBox.No
        )

        msg.setDefaultButton(QMessageBox.No)

        return msg.exec()

    def update_categories(self):
        type_ = self.type_input.currentText()

        self.categorie_input.clear()

        if type_ == "revenu":
            self.categorie_input.addItems(["Salaire", "Freelance", "Autre"])
        else:
            self.categorie_input.addItems(
                ["Food", "Transport", "Logement", "Autre"])

    def update_table(self, data):
        self.table.setRowCount(0)
        self.table.setColumnCount(7)

        for row_number, row_data in enumerate(data):
            self.table.insertRow(row_number)

            # numéro affiché (1,2,3...)
            self.table.setItem(
                row_number, 0, QTableWidgetItem(str(row_number + 1)))

            for column_number, value in enumerate(row_data):
                self.table.setItem(
                    row_number,
                    column_number + 1,  # +1 car la première colonne est pour le numéro
                    QTableWidgetItem(str(value))
                )

    def update_totaux(self, revenus, depenses):
        revenus = revenus or 0
        depenses = depenses or 0

        solde = revenus - depenses

        self.total_revenus_label.setText(f"Total revenus: {revenus}")
        self.total_depenses_label.setText(f"Total dépenses: {depenses}")
        self.solde_label.setText(f"Solde: {solde}")

    def show_message(self, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.exec()

    def clear_inputs(self):
        self.montant_input.clear()
        self.description_input.clear()
        self.date_input.setDate(QDate.currentDate())
