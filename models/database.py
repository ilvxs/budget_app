try:
    import mysql.connector
except ImportError as err:
    raise ImportError(
        "mysql.connector module not found. Install mysql-connector-python with pip."
    ) from err


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="budget_db"
    )


def get_all_transactions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions")
    data = cursor.fetchall()

    conn.close()
    return data


def insert_transaction(type, montant, categorie, description, date):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO transactions (type, montant, categorie, description, date)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, (type, montant, categorie, description, date))
    conn.commit()
    conn.close()


def delete_transaction(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM transactions WHERE id = %s", (id,))
    conn.commit()
    conn.close()


# Filtre par catégorie, mois et année

def get_transactions_filtered(month, year, categorie):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM transactions WHERE 1=1"
    params = []

    if month != "Tous":
        query += " AND MONTH(date) = %s"
        params.append(month)
    if year != "Tous":
        query += " AND YEAR(date) = %s"
        params.append(year)

    if categorie != "Toutes":
        query += " AND categorie = %s"
        params.append(categorie)

    cursor.execute(query, tuple(params))

    data = cursor.fetchall()
    conn.close()
    return data


def get_totaux(month, year, categorie):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            SUM(CASE WHEN type='revenu' THEN montant ELSE 0 END),
            SUM(CASE WHEN type='depense' THEN montant ELSE 0 END)
        FROM transactions
        WHERE 1=1
    """
    params = []

    if month != "Tous":
        query += " AND MONTH(date) = %s"
        params.append(month)

    if year != "Tous":
        query += " AND YEAR(date) = %s"
        params.append(year)

    if categorie != "Toutes":
        query += " AND categorie = %s"
        params.append(categorie)

    cursor.execute(query, tuple(params))

    result = cursor.fetchone()
    conn.close()
    return result
