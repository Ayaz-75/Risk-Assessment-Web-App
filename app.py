import sqlite3
import pandas as pd
import random

# Generate synthetic data
def generate_data(num_records=100):
    data = {
        "Customer_ID": [f"CUST{str(i).zfill(4)}" for i in range(1, num_records + 1)],
        "Credit_Score": [random.randint(300, 850) for _ in range(num_records)],
        "Income": [random.randint(30000, 150000) for _ in range(num_records)],
        "Debt": [random.randint(1000, 50000) for _ in range(num_records)],
        "Loan_Amount": [random.randint(5000, 50000) for _ in range(num_records)],
        "Risk_Score": [random.uniform(0, 1) for _ in range(num_records)],
    }
    return pd.DataFrame(data)

import snowflake.connector

# Replace these with your Snowflake credentials
account = 'xy12345'  # Your Snowflake account name (e.g., 'xy12345.snowflakecomputing.com')
user = 'YOUR_USERNAME'  # Your Snowflake username
password = 'YOUR_PASSWORD'  # Your Snowflake password
warehouse = 'RISK_WH'  # Your Snowflake warehouse name
database = 'RiskAssessmentDB'  # Your Snowflake database name
schema = 'RiskAssessmentSchema'  # Your Snowflake schema name

# Establish the connection
conn = snowflake.connector.connect(
    user=user,
    password=password,
    account=account,
    warehouse=warehouse,
    database=database,
    schema=schema
)

# Create a cursor object to interact with Snowflake
cursor = conn.cursor()

# Example query: Show tables in the current schema
cursor.execute("SHOW TABLES;")

# Fetch and print the results
tables = cursor.fetchall()
for table in tables:
    print(table)

# Close the cursor and connection
cursor.close()
conn.close()


# Save dataset to CSV (optional)
data = generate_data()
data.to_csv("synthetic_financial_data.csv", index=False)

# Connect to SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('risk_assessment.db')
cursor = conn.cursor()

# Create the RiskAssessment table if it doesn't exist
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

# Insert data into SQLite
for index, row in data.iterrows():
    cursor.execute('''
        INSERT INTO RiskAssessment (Customer_ID, Credit_Score, Income, Debt, Loan_Amount, Risk_Score)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (row['Customer_ID'], row['Credit_Score'], row['Income'], row['Debt'], row['Loan_Amount'], row['Risk_Score']))

# Commit the changes
conn.commit()

print("Data successfully loaded into SQLite!")

# Query data from SQLite
cursor.execute("SELECT * FROM RiskAssessment LIMIT 10;")
rows = cursor.fetchall()

# Display fetched data
for row in rows:
    print(row)

# Close the connection
conn.close()
