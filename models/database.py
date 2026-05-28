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


def get_all_transactions(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions WHERE user_id = %s", (user_id,))
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data


def insert_transaction(type_, montant, categorie, description, date, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO transactions (type, montant, categorie, description, date, user_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (type_, montant, categorie,
                   description, date, user_id))
    conn.commit()

    cursor.close()
    conn.close()


def delete_transaction(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM transactions WHERE id = %s", (id,))
    conn.commit()
    conn.close()


# Filtre par catégorie, mois et année

def get_transactions_filtered(user_id, month, year, categorie):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT * FROM transactions
    WHERE user_id = %s
    """

    params = [user_id]

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

    cursor.close()
    conn.close()

    return data


def get_totaux(user_id, month, year, categorie):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            SUM(CASE WHEN type='revenu' THEN montant ELSE 0 END),
            SUM(CASE WHEN type='depense' THEN montant ELSE 0 END)
        FROM transactions
        WHERE user_id = %s
    """

    params = [user_id]

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

    cursor.close()
    conn.close()

    return result


def check_user(username, password):
    connection = get_connection()

    cursor = connection.cursor()

    query = """
    SELECT * FROM users
    WHERE username = %s AND password = %s
    """

    cursor.execute(query, (username, password))

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return {
        "id": user[0],
        "username": user[1]
    } if user else None


def get_dashboard_data(user_id):

    connection = get_connection()

    cursor = connection.cursor()

    # revenus
    cursor.execute("""
        SELECT SUM(montant)
        FROM transactions
        WHERE type='revenu'
        AND user_id=%s
    """, (user_id,))

    revenus = cursor.fetchone()[0] or 0

    # dépenses
    cursor.execute("""
        SELECT SUM(montant)
        FROM transactions
        WHERE type='depense'
        AND user_id=%s
    """, (user_id,))

    depenses = cursor.fetchone()[0] or 0

    # total transactions
    cursor.execute("""
        SELECT COUNT(*)
        FROM transactions
        WHERE user_id=%s
    """, (user_id,))

    transactions = cursor.fetchone()[0]

    connection.close()

    return revenus, depenses, transactions


def get_expenses_by_category(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT categorie, SUM(montant)
        FROM transactions
        WHERE type='depense'
        AND user_id=%s
        GROUP BY categorie
        """, (user_id,))

    data = cursor.fetchall()

    conn.close()

    return data
