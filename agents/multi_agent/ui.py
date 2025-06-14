from collections import defaultdict
import streamlit as st
import yfinance as yf
from groq import Groq
import requests
import json
import os
import json
import traceback

# === Set your Groq API key ===
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

mock_transactions = [
    {"date": "2025-05-01", "category": "Food", "amount": 180},
    {"date": "2025-05-03", "category": "Transport", "amount": 70},
    {"date": "2025-05-04", "category": "Rent", "amount": 500},
    {"date": "2025-05-10", "category": "Entertainment", "amount": 60},
    {"date": "2025-05-15", "category": "Utilities", "amount": 100},
    {"date": "2025-05-20", "category": "Food", "amount": 150},
    {"date": "2025-05-23", "category": "Subscriptions", "amount": 40},
    {"date": "2025-05-26", "category": "Transport", "amount": 60},
]


### ------------------------
### 1. Personalized Financial Analysis
### ------------------------

def analyze_transactions(transactions):
    category_totals = defaultdict(float)
    for tx in transactions:
        category_totals[tx["category"]] += tx["amount"]
    
    sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    return {
        "summary": category_totals,
        "sorted": sorted_categories,
        "ready_for_visualization": [{"category": k, "amount": v} for k, v in sorted_categories]
    }

### ------------------------
### 2. Smart Budgeting & Saving Suggestions
### ------------------------

def get_budget_recommendation(transactions_summary):
    prompt = f"""
    Based on the following transaction summary, generate a personalized budget plan
    for the upcoming month. Include savings, flexible spending, and essential categories.
    
    Transaction Summary: {transactions_summary}
    
    Response format:
    - Monthly Budget Overview
    - Key Areas of Overspending
    - Savings Tips
    """

    response = client.chat.completions.create(
        # - llama3-70b-8192
        # - llama3-8b-8192
        # - gemma-7b-it

        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are a financial budgeting assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()


### ------------------------
### 3. Investment Guidance
### ------------------------

def get_investment_advice(prompt):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are a robo-investor advisor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()


### ------------------------
### 4. Interface with Core Banking & Simulated Investment
### ------------------------

def fetch_transactions_from_api(api_url, headers):
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching transactions: {response.status_code}")

def execute_investment(api_url, payload, headers):
    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Investment failed: {response.status_code}")



# === Streamlit UI ===

st.set_page_config(page_title="Fintech AI Agent 💸", page_icon="💹")
st.title("💸 Fintech Agent Dashboard")
st.subheader("Empowering you to make smarter financial decisions")

# Sidebar menu
option = st.sidebar.selectbox(
    "Select a feature",
    ("📈 Analyze transactions", 
     "💹 Get budget recommendation", 
     "📈 Investment guidance")
)

# === Feature 1: Analyze transactions ===
if option == "📈 Analyze transactions":
    st.header("📈 Analyze transactions")

    if st.button("Analyze"):
        analysis_result = analyze_transactions(mock_transactions)
        st.success(json.dumps(analysis_result["ready_for_visualization"], indent=2))

# === Feature 2: Budget recommendation ===
elif option == "💹 Get budget recommendation":
    st.header("💹 Get budget recommendation")
    budget_amount = st.text_input("Enter the amount you would like to budget recommendation for")

    def generate_budget_prompt(budget_amount):
        total_income = budget_amount
        prompt = f"""
    You are a financial assistant. Here is the user's income data (monthly):
    {total_income}

    Based on this, suggest:
    1. A monthly budget for each category
    2. One saving goal
    3. Tips to stick to the budget
    """
        return prompt


    if st.button("Budget"):
        try:
            prompt = generate_budget_prompt(budget_amount)
            budget_response = get_budget_recommendation(prompt)

            st.success(f"Your budget recommendation is: {budget_response}")
        except Exception as e:
            traceback.print_exc()
            st.error("⚠️ Failed to fetch budget recommendation. Try another amount.")

# === Feature 3: Financial Term Explainer ===
elif option == "📈 Investment guidance":
    st.header("📈 Investment guidance")
    age = st.text_input("how old are you?")
    risk_appetite = st.selectbox("What is your risk appetite?", ["Low", "Moderate", "High"])
    goal = st.text_input("What is your investment goal?")
    monthly_investment = st.number_input("How much can you invest monthly?", min_value=0)
    
    user_profile = {
        "age": age,
        "risk_appetite": risk_appetite,
        "goal": goal,
        "monthly_investment": monthly_investment
    }

    def generate_investment_prompt(user_profile):
        prompt = f"""
    You are a robo-investor advisor. Here is the user's profile:
    - Age: {user_profile['age']}
    - Risk Appetite: {user_profile['risk_appetite']}
    - Goal: {user_profile['goal']}
    - Monthly Investment Capacity: ${user_profile['monthly_investment']}

    Recommend a diversified ETF or stock portfolio.
    Explain why each asset is chosen.
    """
        return prompt
    
    if st.button("Advise"):
        try:
            investment_prompt = generate_investment_prompt(user_profile)
            investment_response = get_investment_advice(investment_prompt)
            st.info(investment_response)
        except Exception as e:
            st.error("⚠️ Could not fetch explanation. Check your API key or try again.")

# Footer
st.markdown("---")
st.markdown("🚀 Built with Python, Streamlit, Groq & Yahoo Finance")