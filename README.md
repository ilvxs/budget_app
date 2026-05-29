# Budget AI — Intelligent Budget Management Desktop App

Budget AI is a desktop application built with **Python**, **PySide6**, **MySQL**, **QtCharts**, **OpenPyXL**, and **Gemini API**.

The application helps users manage personal finances, analyze spending behavior, detect unusual expenses, visualize budget data, and ask an AI assistant questions about their financial situation.

---

## 1. Main Features

### Authentication
- Login screen
- MySQL-based users table
- Multi-user support
- Each user has their own private transactions

### Transaction Management
- Add revenue and expense transactions
- Delete selected transactions
- Confirm delete popup
- Automatic current date, with manual date modification
- Dynamic categories depending on transaction type
- Input validation
- Clear fields after adding a transaction

### Filters
- Filter transactions by:
  - month
  - year
  - category
- Totals update according to selected filters

### Dashboard
- Total revenues card
- Total expenses card
- Solde card
- Transaction count card
- Monthly overview chart
- Expense categories pie chart

### Analytics
- Spending evolution graph
- Dynamic AI Insights cards
- Biggest expense category for the current month
- Average monthly expense
- Current month vs previous month comparison
- Estimated savings for the current month
- Anomaly detection:
  - high individual expenses
  - monthly spending spikes
  - category overspending compared to previous monthly average

### AI Financial Assistant
- Real AI assistant using Gemini API
- Uses the current user's financial data as context
- Can answer questions about:
  - expenses
  - revenues
  - savings
  - anomalies
  - biggest spending categories
  - budget improvement
- Designed to focus on personal finance questions

### Export
- Export transactions to Excel

---

## 2. Technologies Used

```text
Python
PySide6
MySQL / MariaDB
XAMPP
QtCharts
OpenPyXL
Matplotlib
Google Gemini API
```

---

## 3. Project Structure

```text
budget_app/
│
├── controllers/
│   ├── login_controller.py
│   ├── budget_controller.py
│   ├── dashboard_controller.py
│   ├── analytics_controller.py
│   └── ai_assistant_controller.py
│
├── models/
│   ├── database.py
│   └── transaction.py
│
├── services/
│   └── gemini_service.py
│
├── views/
│   ├── login_window.py
│   ├── main_window.py
│   │
│   └── pages/
│       ├── transactions_page.py
│       ├── dashboard_page.py
│       ├── analytics_page.py
│       ├── ai_assistant_page.py
│       └── settings_page.py
│
├── assets/
│   └── icon.png
│
├── main.py
├── demo_data.sql
└── README.md
```

---

## 4. Installation

Install required Python libraries:

```bash
pip install PySide6 mysql-connector-python openpyxl matplotlib google-genai
```

If you are using the old Gemini SDK, you may also have:

```bash
pip install google-generativeai
```

However, the recommended package is:

```bash
pip install google-genai
```

---

## 5. Database Setup

Start **MySQL** from **XAMPP**.

Open MySQL terminal or phpMyAdmin and create the database:

```sql
CREATE DATABASE budget_db;
USE budget_db;
```

Create the users table:

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
```

Create the transactions table:

```sql
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(20) NOT NULL,
    montant DECIMAL(10,2) NOT NULL,
    categorie VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    date DATE NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

---

## 6. Demo Data

A demo file is provided:

```text
demo_data.sql
```

It creates only two demo users:

```text
admin / 1234
test  / 1234
```

It inserts many transactions for both users across five months.

The demo data is designed to test:

- multi-user isolation
- dashboard cards
- dashboard charts
- transaction filters
- analytics insights
- spending evolution
- anomaly detection
- AI assistant responses

### Import demo data using phpMyAdmin

1. Open XAMPP
2. Start Apache and MySQL
3. Open:

```text
http://localhost/phpmyadmin
```

4. Select the database:

```text
budget_db
```

5. Click **Import**
6. Choose:

```text
demo_data.sql
```

7. Click **Go**

### Import demo data using terminal

```bash
mysql -u root -p budget_db < demo_data.sql
```

If your XAMPP root password is empty, press Enter when asked for a password.

---

## 7. Gemini API Setup

The AI assistant uses Gemini API.

Create an API key from Google AI Studio:

```text
https://aistudio.google.com/app/apikey
```

In the project, open:

```text
services/gemini_service.py
```

Example Gemini service:

```python
from google import genai

client = genai.Client(
    api_key="YOUR_GEMINI_API_KEY"
)

def ask_ai(prompt):
    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt
    )

    return response.text
```

Recommended free model:

```text
gemini-flash-lite-latest
```

---

## 8. How to Run the App

Make sure MySQL is running from XAMPP.

Then run:

```bash
python main.py
```

Login with one of the demo accounts:

```text
admin / 1234
```

or:

```text
test / 1234
```

---

## 9. How to Use the AI Assistant

The assistant receives the current user's financial context, including:

- current month revenues
- current month expenses
- previous month expenses
- average monthly expenses
- biggest expense category
- category distribution
- recent transactions

Example questions:

```text
Why are my expenses high this month?
How can I reduce my expenses?
What is my biggest expense category?
Am I saving enough this month?
Analyze my financial situation.
Do I have any unusual expenses?
Compare this month with last month.
What should I improve in my budget?
```

The assistant is designed to answer finance-related questions.  
For unrelated questions, the prompt can be configured to politely refuse and say that it only helps with budget and financial data.

---

## 10. Anomaly Detection Logic

The Analytics page detects anomalies using three rules.

### High Individual Expense

Example:

```text
A single transaction is greater than or equal to 2000 MAD.
```

This triggers a warning like:

```text
High expense detected: 2500 MAD in Food.
```

### Monthly Spending Spike

The app compares current month expenses with previous month expenses.

If:

```text
increase > 40%
```

it shows a warning.

Example:

```text
Expenses increased by 60% compared to last month.
```

### Category Abuse Detection

The app compares current month spending in a category with the average of previous months.

If:

```text
current category total > previous average + 50%
```

it shows a warning.

Example:

```text
Category anomaly detected: Transport
This month's spending: 1200 MAD
Previous monthly average: 300 MAD
Increase: 300% above normal
```

---

## 11. Architecture Explanation

The project follows a clean separation of responsibilities.

### Views

Located in:

```text
views/
```

They contain UI components only.

### Controllers

Located in:

```text
controllers/
```

They connect UI actions to business logic.

### Models

Located in:

```text
models/
```

They handle database access and data structures.

### Services

Located in:

```text
services/
```

They handle external services such as Gemini API.

---

## 12. Future Improvements

Possible future upgrades:

- Register screen
- Dark mode
- Budget goals
- Notifications
- More advanced prediction system
- Better AI memory and conversation history
