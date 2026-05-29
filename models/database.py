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


def get_monthly_expenses(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT MONTH(date), SUM(montant)
    FROM transactions
    WHERE user_id = %s
    AND type = 'depense'
    GROUP BY MONTH(date)
    ORDER BY MONTH(date)
    """, (user_id,))

    data = cursor.fetchall()

    conn.close()

    return data


def get_biggest_expense_category(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT categorie, SUM(montant) as total
        FROM transactions
        WHERE user_id = %s
        AND type = 'depense'
        AND MONTH(date) = MONTH(CURRENT_DATE())
        AND YEAR(date) = YEAR(CURRENT_DATE())
        GROUP BY categorie
        ORDER BY total DESC
        LIMIT 1
        """, (user_id,))

    result = cursor.fetchone()

    conn.close()

    return result


def get_average_monthly_expense(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT AVG(month_total)
    FROM (
        SELECT SUM(montant) as month_total
        FROM transactions
        WHERE user_id = %s
        AND type = 'depense'
        GROUP BY YEAR(date), MONTH(date)
    ) as monthly_expenses
    """, (user_id,))

    result = cursor.fetchone()[0]

    conn.close()

    return result or 0


def get_total_expenses(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(montant)
    FROM transactions
    WHERE user_id = %s
    AND type = 'depense'
    """, (user_id,))

    total = cursor.fetchone()[0]

    conn.close()

    return total or 0


def get_total_revenues(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(montant)
    FROM transactions
    WHERE user_id = %s
    AND type = 'revenu'
    """, (user_id,))

    total = cursor.fetchone()[0]

    conn.close()

    return total or 0


def get_high_expenses(user_id):

    connect = get_connection()
    cursor = connect.cursor()

    cursor.execute("""
    SELECT categorie, montant, date
    FROM transactions
    WHERE user_id = %s
    AND type = 'depense'
    ORDER BY montant DESC
    LIMIT 5
    """, (user_id,))

    data = cursor.fetchall()

    connect.close()

    return data


def get_current_month_revenues(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(montant)
    FROM transactions
    WHERE user_id = %s
    AND type = 'revenu'
    AND MONTH(date) = MONTH(CURRENT_DATE())
    AND YEAR(date) = YEAR(CURRENT_DATE())
    """, (user_id,))

    total = cursor.fetchone()[0]

    conn.close()

    return total or 0


def get_current_month_expenses(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(montant)
        FROM transactions
        WHERE user_id = %s
        AND type = 'depense'
        AND MONTH(date) = MONTH(CURRENT_DATE())
        AND YEAR(date) = YEAR(CURRENT_DATE())
        """, (user_id,))

    result = cursor.fetchone()[0]

    conn.close()

    return result or 0


def get_previous_month_expenses(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(montant)
    FROM transactions
    WHERE user_id = %s
    AND type = 'depense'
    AND MONTH(date) = MONTH(CURRENT_DATE() - INTERVAL 1 MONTH)
    AND YEAR(date) = YEAR(CURDATE() - INTERVAL 1 MONTH)
    """, (user_id,))

    result = cursor.fetchone()[0]

    conn.close()

    return result or 0


def get_category_average(user_id, category):

    connect = get_connection()
    cursor = connect.cursor()

    cursor.execute("""
    SELECT AVG(month_total)
    FROM (
        SELECT SUM(montant) as month_total
        FROM transactions
        WHERE user_id = %s
        AND type = 'depense'
        AND categorie = %s
        AND NOT (
            MONTH(date) = MONTH(CURDATE())
            AND YEAR(date) = YEAR(CURDATE())
        )
        GROUP BY YEAR(date), MONTH(date)
    ) as monthly_data
    """, (user_id, category))

    result = cursor.fetchone()[0]

    connect.close()

    return result or 0


def get_current_month_categories(user_id):

    connect = get_connection()
    cursor = connect.cursor()

    cursor.execute("""
    SELECT categorie, SUM(montant)
    FROM transactions
    WHERE user_id = %s
    AND type = 'depense'
    AND MONTH(date) = MONTH(CURDATE())
    AND YEAR(date) = YEAR(CURDATE())
    GROUP BY categorie
    """, (user_id,))

    data = cursor.fetchall()

    connect.close()

    return data
