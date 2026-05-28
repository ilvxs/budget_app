from models import database
import matplotlib.pyplot as plt
from openpyxl import Workbook
from PySide6.QtWidgets import QMessageBox


class BudgetController:
    def __init__(self, view, user, main_window, dashboard_controller, analytics_controller):
        self.view = view
        self.user = user
        self.main_window = main_window
        self.dashboard_controller = dashboard_controller
        self.analytics_controller = analytics_controller

        # connecter les boutons
        self.view.add_button.clicked.connect(self.ajouter_transaction)
        self.view.delete_button.clicked.connect(self.supprimer_transaction)
        self.view.filter_button.clicked.connect(self.filtrer_transactions)
        self.view.chart_button.clicked.connect(self.show_chart)
        self.view.export_button.clicked.connect(self.export_excel)
        self.main_window.logout_button.clicked.connect(self.logout)

        # charger données au démarrage
        self.charger_transactions()

    def mettre_a_jour_totaux(self):
        # On récupère les textes directement
        month = self.view.month_filter.currentText()
        year = self.view.year_filter.currentText()
        categorie = self.view.category_filter.currentText()

        revenus, depenses = database.get_totaux(
            self.user["id"],
            month,
            year,
            categorie
        )
        self.view.update_totaux(revenus, depenses)

    def ajouter_transaction(self):
        montant = self.view.montant_input.text()
        type_ = self.view.type_input.currentText()
        categorie = self.view.categorie_input.currentText()
        description = self.view.description_input.text()
        date = self.view.date_input.date().toString("yyyy-MM-dd")

        # message + validation
        if not montant:
            self.view.show_message("Le montant est obligatoire")
            return

        try:
            montant = float(montant)
        except:
            self.view.show_message("Montant invalide")
            return

        database.insert_transaction(
            type_,
            montant,
            categorie,
            description,
            date,
            self.user["id"]
        )

        # vider les champs + message et recharger les données
        self.view.clear_inputs()
        self.view.show_message("Transaction ajoutée ✅")
        self.charger_transactions()
        self.dashboard_controller.load_dashboard()
        self.analytics_controller.load_analytics()

        self.dashboard_controller.load_dashboard()

    def charger_transactions(self):
        # Au lieu de charger TOUTES les données, on lance directement le filtre.
        # Ainsi, le tableau et les totaux seront parfaitement synchronisés avec les menus déroulants.
        self.filtrer_transactions()
        # REFRESH DASHBOARD AUTOMATICALLY
        self.update_dashboard()

    def supprimer_transaction(self):
        selected = self.view.table.currentRow()

        if selected == -1:
            self.view.show_message("Sélectionnez une transaction")
            return

        # colonne 1 = vrai ID
        id_item = self.view.table.item(selected, 1)

        if id_item is None:
            return

        id_ = int(id_item.text())

        confirmation = self.view.confirm_delete()

        if confirmation == QMessageBox.Yes:
            database.delete_transaction(id_)

            self.charger_transactions()
            self.dashboard_controller.load_dashboard()
            self.analytics_controller.load_analytics()

            self.dashboard_controller.load_dashboard()

            self.view.show_message("Transaction supprimée ✅")

    def filtrer_transactions(self):
        month = self.view.month_filter.currentText()
        year = self.view.year_filter.currentText()
        categorie = self.view.category_filter.currentText()

        data = database.get_transactions_filtered(
            self.user["id"], month, year, categorie)
        self.view.update_table(data)

        self.mettre_a_jour_totaux()

    # afficher un graphique
    def show_chart(self):
        month = self.view.month_filter.currentText()
        year = self.view.year_filter.currentText()
        categorie = self.view.category_filter.currentText()

        revenus, depenses = database.get_totaux(
            self.user["id"],
            month,
            year,
            categorie
        )

        # Nettoyage des valeurs (remplacer None par 0)
        revenus_propres = revenus or 0
        depenses_propres = depenses or 0

        # Vérification : si tout est à 0, on annule l'affichage
        if revenus_propres == 0 and depenses_propres == 0:
            self.view.show_message(
                "Aucune donnée à afficher pour cette période.")
            return

        labels = ['Revenus', 'Dépenses']
        values = [revenus_propres, depenses_propres]

        # Nettoyer l'ancienne figure pour éviter la superposition si on clique plusieurs fois
        plt.clf()

        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title("Répartition Budget")
        plt.show()

    # exporter les données vers Excel
    def export_excel(self):
        data = database.get_all_transactions(
            self.user["id"]
        )

        wb = Workbook()
        ws = wb.active

        ws.append(["ID", "Type", "Montant", "Catégorie", "Description", "Date"])

        for row in data:
            ws.append(row)

        wb.save("transactions.xlsx")

        self.view.show_message("Export Excel réussi ✅")

    def logout(self):
        reply = QMessageBox.question(
            self.view,
            "Logout",
            "Voulez-vous vous déconnecter ?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:

            # local imports to avoid circular import
            from views.login_window import LoginWindow
            from controllers.login_controller import LoginController

            # open login
            self.login_window = LoginWindow()

            self.login_controller = LoginController(
                self.login_window
            )

            self.login_window.show()

            # close dashboard
            self.main_window.close()

    def update_dashboard(self):
        revenus, depenses, transactions = database.get_dashboard_data(
            self.user["id"]
        )

        self.main_window.dashboard_page.update_cards(
            revenus,
            depenses,
            transactions
        )
