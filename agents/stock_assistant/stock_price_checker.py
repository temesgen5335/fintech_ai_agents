import streamlit as st
import yfinance as yf
import math
from groq import Groq

# === Set your Groq API key ===
groq_api_key = "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"
client = Groq(api_key=groq_api_key)

# === Financial Logic Functions ===

def calculate_compound_interest(principal, rate, years):
    amount = principal * (math.pow((1 + rate / 100), years))
    return round(amount, 2)

def fetch_stock_price(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    todays_data = stock.history(period='1d')
    return round(todays_data['Close'][0], 2)

def explain_term_with_groq(term):
    prompt = f"Explain the financial term '{term}' in simple and clear words for a beginner."

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="mixtral-8x7b-32768"
    )

    return chat_completion.choices[0].message.content

# === Streamlit UI ===

st.set_page_config(page_title="Fintech AI Agent 💸", page_icon="💹")
st.title("💸 Fintech Agent Dashboard")
st.subheader("Empowering you to make smarter financial decisions")

# Sidebar menu
option = st.sidebar.selectbox(
    "Select a feature",
    ("📈 Compound Interest Calculator", 
     "💹 Stock Price Checker", 
     "🧠 Explain Financial Term")
)

# === Feature 1: Compound Interest ===
if option == "📈 Compound Interest Calculator":
    st.header("📈 Compound Interest Calculator")

    principal = st.number_input("Principal Amount ($)", min_value=0.0, step=100.0)
    rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, step=0.5)
    years = st.number_input("Investment Duration (Years)", min_value=0.0, step=1.0)

    if st.button("Calculate"):
        future_value = calculate_compound_interest(principal, rate, years)
        st.success(f"Your investment will grow to: **${future_value}**")

# === Feature 2: Stock Price Checker ===
elif option == "💹 Stock Price Checker":
    st.header("💹 Get Live Stock Price")
    ticker = st.text_input("Enter stock symbol (e.g., AAPL, TSLA, GOOG)")

    if st.button("Fetch Price"):
        try:
            price = fetch_stock_price(ticker.upper())
            st.success(f"The current price of **{ticker.upper()}** is **${price}**")
        except Exception as e:
            st.error("⚠️ Failed to fetch stock price. Try another symbol.")

# === Feature 3: Financial Term Explainer ===
elif option == "🧠 Explain Financial Term":
    st.header("🧠 Explain Financial Terms with AI")
    term = st.text_input("Enter a financial term (e.g., inflation, mutual fund)")

    if st.button("Explain"):
        try:
            explanation = explain_term_with_groq(term)
            st.info(explanation)
        except Exception as e:
            st.error("⚠️ Could not fetch explanation. Check your API key or try again.")

# Footer
st.markdown("---")
st.markdown("🚀 Built with Python, Streamlit, Groq & Yahoo Finance")