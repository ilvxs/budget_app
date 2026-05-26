from models import database
import matplotlib.pyplot as plt
from openpyxl import Workbook
from PySide6.QtWidgets import QMessageBox


class BudgetController:
    def __init__(self, view):
        self.view = view

        # connecter les boutons
        self.view.add_button.clicked.connect(self.ajouter_transaction)
        self.view.delete_button.clicked.connect(self.supprimer_transaction)
        self.view.filter_button.clicked.connect(self.filtrer_transactions)
        self.view.chart_button.clicked.connect(self.show_chart)
        self.view.export_button.clicked.connect(self.export_excel)

        # charger données au démarrage
        self.charger_transactions()

    def mettre_a_jour_totaux(self):
        # On récupère les textes directement
        month = self.view.month_filter.currentText()
        year = self.view.year_filter.currentText()
        categorie = self.view.category_filter.currentText()

        revenus, depenses = database.get_totaux(month, year, categorie)
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
            date
        )

        # vider les champs + message et recharger les données
        self.view.clear_inputs()
        self.view.show_message("Transaction ajoutée ✅")
        self.charger_transactions()

    def charger_transactions(self):
        # Au lieu de charger TOUTES les données, on lance directement le filtre.
        # Ainsi, le tableau et les totaux seront parfaitement synchronisés avec les menus déroulants.
        self.filtrer_transactions()

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

            self.view.show_message("Transaction supprimée ✅")

    def filtrer_transactions(self):
        month = self.view.month_filter.currentText()
        year = self.view.year_filter.currentText()
        categorie = self.view.category_filter.currentText()

        data = database.get_transactions_filtered(month, year, categorie)
        self.view.update_table(data)

        self.mettre_a_jour_totaux()

    # afficher un graphique
    def show_chart(self):
        month = self.view.month_filter.currentText()
        year = self.view.year_filter.currentText()
        categorie = self.view.category_filter.currentText()

        revenus, depenses = database.get_totaux(
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
        data = database.get_all_transactions()

        wb = Workbook()
        ws = wb.active

        ws.append(["ID", "Type", "Montant", "Catégorie", "Description", "Date"])

        for row in data:
            ws.append(row)

        wb.save("transactions.xlsx")

        self.view.show_message("Export Excel réussi ✅")
