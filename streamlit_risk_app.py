
import openai
import streamlit as st
import sqlite3
from dotenv import load_dotenv
import matplotlib.pyplot as plt

from streamlit_lottie import st_lottie
import requests

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_risk = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json")
st_lottie(lottie_risk, height=300, key="risk_analysis")

# # # OpenAI API key

# # Function to get insights from Mistral AI
# def analyze_risk_with_mistral(credit_score, income, debt, loan_amount):
#     # Construct the prompt with financial data
#     prompt = f"""
#     Given the following financial data:
#     Credit Score: {credit_score}
#     Income: {income}
#     Debt: {debt}
#     Loan Amount: {loan_amount}

#     Please analyze the risk and provide insights on whether the loan should be approved or not.
#     """

#     # Use the new OpenAI API method (completions-based model)
#     response = openai.completions.create(
#         model="gpt-3.5-turbo",  # Use Mistral model or the one you're using
#         prompt=prompt,
#         max_tokens=100  # Adjust the token limit as per your requirements
#     )

#     # Extract and return the response
#     ai_insights = response['choices'][0]['text']
#     return ai_insights
def analyze_risk(credit_score, income, debt, loan_amount):
    # Basic risk analysis logic
    if credit_score < 600:
        risk = "High"
    elif credit_score >= 600 and credit_score < 700:
        risk = "Medium"
    else:
        risk = "Low"

    # Additional risk factors based on income, debt, and loan amount
    if income < 3000 or debt > income * 0.5:
        risk = "High"
    elif loan_amount > income * 3:
        risk = "Medium"

    return risk



# Streamlit app UI
st.title("75th Coder's Risk Assessment App")
st.subheader("Analyze financial risk based on user inputs. Using Snowflake, Streamlit, and Mistral AI.")
st.markdown("This app helps calculate and visualize risk scores for financial decision-making.")


# Input fields for customer data
# Replace the existing input fields with:
st.sidebar.header("Input Parameters")
credit_score = st.sidebar.slider("Credit Score", min_value=300, max_value=850, value=700)
income = st.sidebar.slider("Income ($)", min_value=10000, max_value=200000, step=1000, value=50000)
debt = st.sidebar.slider("Debt ($)", min_value=0, max_value=50000, step=1000, value=10000)
loan_amount = st.sidebar.slider("Loan Amount ($)", min_value=5000, max_value=50000, step=1000, value=20000)

# customer_id = st.text_input("Customer ID")
# credit_score = st.number_input("Credit Score", min_value=300, max_value=850)
# income = st.number_input("Income", min_value=0)
# debt = st.number_input("Debt", min_value=0)
# loan_amount = st.number_input("Loan Amount", min_value=0)

# Calculate risk score and get AI analysis
# if st.button("Analyze Risk"):
#     # Calculate a simple risk score
#     risk_score = (loan_amount / income) * (debt / credit_score)
#     st.write(f"Calculated Risk Score: {risk_score:.2f}")
if st.button("Analyze Risk"):
    risk = analyze_risk(credit_score, income, debt, loan_amount)
    st.write(f"Risk Assessment: {risk}")

    # Mapping risk to a numeric value for the bar chart
    risk_score = {"High": 3, "Medium": 2, "Low": 1}[risk]
    
    # Create a bar chart based on the risk score
    labels = ['High', 'Medium', 'Low']
    values = [3, 2, 1]  # Corresponding values for each risk level
    risk_values = [0, 0, 0]
    risk_values[risk_score - 1] = 1  # Mark the selected risk level as 1

    fig, ax = plt.subplots()
    ax.bar(labels, risk_values, color=['red', 'yellow', 'green'])
    ax.set_title('Risk Assessment Visualization')
    ax.set_ylabel('Risk Level')
    ax.set_ylim(0, 1)
    
    # Display the graph
    st.pyplot(fig)


if income == 0 or credit_score == 0:
    st.error("Income and Credit Score must be greater than zero to calculate the risk score.")
else:
    risk_score = (loan_amount / income) * (debt / credit_score)
    st.write(f"Calculated Risk Score: {risk_score:.2f}")
    
    # Get AI insights
    # ai_insights = analyze_risk_with_mistral(credit_score, income, debt, loan_amount)
    st.subheader("Mistral AI Analysis")
    # st.write(ai_insights)

import matplotlib.pyplot as plt

# Generate a bar chart for visualization
def plot_risk_visualization(credit_score, income, debt, loan_amount, risk_score):
    categories = ['Credit Score', 'Income', 'Debt', 'Loan Amount', 'Risk Score']
    values = [credit_score, income, debt, loan_amount, risk_score]

    fig, ax = plt.subplots()
    ax.bar(categories, values, color=['blue', 'green', 'red', 'purple', 'orange'])
    ax.set_title("Risk Assessment Visualization")
    ax.set_ylabel("Values")
    st.pyplot(fig)

# Call the visualization function
if income > 0 and credit_score > 0:
    risk_score = (loan_amount / income) * (debt / credit_score)
    st.write(f"Calculated Risk Score: {risk_score:.2f}")
    plot_risk_visualization(credit_score, income, debt, loan_amount, risk_score)

# import streamlit as st
# import sqlite3

# # Function to insert data into the SQLite database
# def insert_data(customer_id, credit_score, income, debt, loan_amount, risk_score):
#     conn = sqlite3.connect('risk_assessment.db')
#     cursor = conn.cursor()
#     cursor.execute('''
#         INSERT INTO RiskAssessment (Customer_ID, Credit_Score, Income, Debt, Loan_Amount, Risk_Score)
#         VALUES (?, ?, ?, ?, ?, ?)
#     ''', (customer_id, credit_score, income, debt, loan_amount, risk_score))
#     conn.commit()
#     conn.close()

# # Function to calculate risk score (simple example)
# def calculate_risk_score(credit_score, income, debt, loan_amount):
#     # Example formula for calculating risk score (you can modify this as per your requirements)
#     risk_score = (loan_amount / income) * (debt / credit_score)
#     return risk_score

# # Streamlit app UI
# st.title("Risk Assessment App")

# # Input fields for customer data
# customer_id = st.text_input("Customer ID")
# credit_score = st.number_input("Credit Score", min_value=300, max_value=850)
# income = st.number_input("Income", min_value=0)
# debt = st.number_input("Debt", min_value=0)
# loan_amount = st.number_input("Loan Amount", min_value=0)

# # Calculate risk score when the button is clicked
# if st.button("Calculate Risk Score"):
#     risk_score = calculate_risk_score(credit_score, income, debt, loan_amount)
#     st.write(f"Calculated Risk Score: {risk_score:.2f}")
    
#     # Insert data into the database
#     insert_data(customer_id, credit_score, income, debt, loan_amount, risk_score)
#     st.success("Data inserted into the database successfully!")

# # Display the data from the database
# st.subheader("Existing Risk Assessment Data")
# conn = sqlite3.connect('risk_assessment.db')
# cursor = conn.cursor()
# cursor.execute('SELECT * FROM RiskAssessment')
# rows = cursor.fetchall()
# for row in rows:
#     st.write(row)
# conn.close()
st.markdown("---")
st.markdown("**Developed by Ayaz Ali & Ayaz Ali| Powered by Streamlit**")
