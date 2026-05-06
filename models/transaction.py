class Transaction:
    def __init__(self, id, type, montant, categorie, description, date):
        self.id = id
        self.type = type
        self.montant = montant
        self.categorie = categorie
        self.description = description
        self.date = date
