import sqlite3

# Connect to SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('risk_assessment.db')
cursor = conn.cursor()

# Create the RiskAssessment table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS RiskAssessment (
        Customer_ID TEXT,
        Credit_Score INTEGER,
        Income INTEGER,
        Debt INTEGER,
        Loan_Amount INTEGER,
        Risk_Score REAL
    )
''')


def insert_data(customer_id, credit_score, income, debt, loan_amount, risk_score, ai_insights):
    conn = sqlite3.connect('risk_assessment.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO RiskAssessment (Customer_ID, Credit_Score, Income, Debt, Loan_Amount, Risk_Score, AI_Insights)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (customer_id, credit_score, income, debt, loan_amount, risk_score, ai_insights))
    conn.commit()
    conn.close()




# Commit and close the connection
conn.commit()
conn.close()

print("Database and table created successfully.")
