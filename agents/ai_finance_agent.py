import os
from groq import Groq
import json
import openai
from datetime import datetime
from collections import defaultdict
import requests

openai.api_key = "YOUR_OPENAI_API_KEY"

### ------------------------
### Mock Data (User Transactions)
### ------------------------

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

def generate_budget_prompt(analysis_result):
    spending_summary = json.dumps(analysis_result["summary"])
    prompt = f"""
You are a financial assistant. Here is the user's spending data (monthly):
{spending_summary}

Based on this, suggest:
1. A monthly budget for each category
2. One saving goal
3. Tips to stick to the budget
"""
    return prompt

def get_budget_recommendation(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]

### ------------------------
### 3. Investment Guidance
### ------------------------

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

def get_investment_advice(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]

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

### ------------------------
### Example Usage
### ------------------------

if __name__ == '__main__':
    print("--- Financial Analysis ---")
    analysis_result = analyze_transactions(mock_transactions)
    print(json.dumps(analysis_result["ready_for_visualization"], indent=2))

    print("\n--- Budget & Saving Suggestion ---")
    budget_prompt = generate_budget_prompt(analysis_result)
    budget_response = get_budget_recommendation(budget_prompt)
    print(budget_response)

    print("\n--- Investment Advice ---")
    user_profile = {
        "age": 30,
        "risk_appetite": "Moderate",
        "goal": "Retirement savings",
        "monthly_investment": 300
    }
    investment_prompt = generate_investment_prompt(user_profile)
    investment_response = get_investment_advice(investment_prompt)
    print(investment_response)

    # Uncomment the following when integrating with real banking/broker systems
    # api_url = "https://yourbankingapi.com/transactions"
    # headers = {"Authorization": "Bearer your_token"}
    # live_transactions = fetch_transactions_from_api(api_url, headers)
    # print(live_transactions)

    # investment_api_url = "https://brokerapi.com/invest"
    # payload = {"amount": 300, "asset": "ETF_XYZ"}
    # result = execute_investment(investment_api_url, payload, headers)
    # print(result)
