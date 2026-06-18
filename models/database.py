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

    cursor.execute("""
        SELECT id, type, amount, category, description, date
        FROM transactions
        WHERE user_id = %s
        ORDER BY date DESC, id DESC
    """, (user_id,))
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data


def insert_transaction(type_, amount, category, description, date, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO transactions (type, amount, category, description, date, user_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (type_, amount, category,
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


# Filter by category, month, and year

def get_transactions_filtered(user_id, month, year, category):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT id, type, amount, category, description, date
    FROM transactions
    WHERE user_id = %s
    """

    params = [user_id]

    if month != "All":
        query += " AND MONTH(date) = %s"
        params.append(month)

    if year != "All":
        query += " AND YEAR(date) = %s"
        params.append(year)

    if category != "All":
        query += " AND category = %s"
        params.append(category)

    query += " ORDER BY date DESC, id DESC"

    cursor.execute(query, tuple(params))

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


def get_totals(user_id, month, year, category):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            SUM(CASE WHEN type='revenue' THEN amount ELSE 0 END),
            SUM(CASE WHEN type='expense' THEN amount ELSE 0 END)
        FROM transactions
        WHERE user_id = %s
    """

    params = [user_id]

    if month != "All":
        query += " AND MONTH(date) = %s"
        params.append(month)

    if year != "All":
        query += " AND YEAR(date) = %s"
        params.append(year)

    if category != "All":
        query += " AND category = %s"
        params.append(category)

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


def username_exists(username):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT id FROM users
    WHERE username = %s
    """

    cursor.execute(query, (username,))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return user is not None


def create_user(username, password):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO users (username, password)
    VALUES (%s, %s)
    """

    cursor.execute(query, (username, password))
    connection.commit()

    cursor.close()
    connection.close()


def get_dashboard_data(user_id):

    connection = get_connection()

    cursor = connection.cursor()

    # revenues
    cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE type='revenue'
        AND user_id=%s
    """, (user_id,))

    revenues = cursor.fetchone()[0] or 0

    # expenses
    cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE type='expense'
        AND user_id=%s
    """, (user_id,))

    expenses = cursor.fetchone()[0] or 0

    # total transactions
    cursor.execute("""
        SELECT COUNT(*)
        FROM transactions
        WHERE user_id=%s
    """, (user_id,))

    transactions = cursor.fetchone()[0]

    connection.close()

    return revenues, expenses, transactions


def get_expenses_by_category(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE type='expense'
        AND user_id=%s
        GROUP BY category
        """, (user_id,))

    data = cursor.fetchall()

    conn.close()

    return data


def get_monthly_expenses(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        YEAR(date),
        MONTH(date),
        SUM(amount)
    FROM transactions
    WHERE user_id = %s
    AND type = 'expense'
    GROUP BY YEAR(date), MONTH(date)
    ORDER BY YEAR(date), MONTH(date)
    """, (user_id,))

    data = cursor.fetchall()

    conn.close()

    return data


def get_biggest_expense_category(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount) as total
        FROM transactions
        WHERE user_id = %s
        AND type = 'expense'
        AND MONTH(date) = MONTH(CURRENT_DATE())
        AND YEAR(date) = YEAR(CURRENT_DATE())
        GROUP BY category
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
        SELECT SUM(amount) as month_total
        FROM transactions
        WHERE user_id = %s
        AND type = 'expense'
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
    SELECT SUM(amount)
    FROM transactions
    WHERE user_id = %s
    AND type = 'expense'
    """, (user_id,))

    total = cursor.fetchone()[0]

    conn.close()

    return total or 0


def get_total_revenues(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(amount)
    FROM transactions
    WHERE user_id = %s
    AND type = 'revenue'
    """, (user_id,))

    total = cursor.fetchone()[0]

    conn.close()

    return total or 0


def get_high_expenses(user_id):

    connect = get_connection()
    cursor = connect.cursor()

    cursor.execute("""
    SELECT category, amount, date
    FROM transactions
    WHERE user_id = %s
    AND type = 'expense'
    ORDER BY amount DESC
    LIMIT 5
    """, (user_id,))

    data = cursor.fetchall()

    connect.close()

    return data


def get_current_month_revenues(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(amount)
    FROM transactions
    WHERE user_id = %s
    AND type = 'revenue'
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
        SELECT SUM(amount)
        FROM transactions
        WHERE user_id = %s
        AND type = 'expense'
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
    SELECT SUM(amount)
    FROM transactions
    WHERE user_id = %s
    AND type = 'expense'
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
        SELECT SUM(amount) as month_total
        FROM transactions
        WHERE user_id = %s
        AND type = 'expense'
        AND category = %s
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
    SELECT category, SUM(amount)
    FROM transactions
    WHERE user_id = %s
    AND type = 'expense'
    AND MONTH(date) = MONTH(CURDATE())
    AND YEAR(date) = YEAR(CURDATE())
    GROUP BY category
    """, (user_id,))

    data = cursor.fetchall()

    connect.close()

    return data
