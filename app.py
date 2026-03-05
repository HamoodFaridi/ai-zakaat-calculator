import streamlit as st
from database import init_db, save_record
from calculator import calculate_zakaat
from ai_explainer import generate_explanation

init_db()

st.title("🕌 AI Zakaat Calculator")

currency = st.selectbox("Select Currency", ["USD", "EUR", "GBP", "INR", "PKR", "AED"])

st.header("💵 Liquid Assets")
cash = st.number_input("Bank and Cash Balance", min_value=0.0)

st.header("📈 Investments")
investments = st.number_input("Stocks / Crypto / Retirement Accounts", min_value=0.0)

st.header("🪙 Precious Metals")
gold = st.number_input("Gold Value", min_value=0.0)
silver = st.number_input("Silver Value", min_value=0.0)

st.header("🏪 Business & Rental")
business = st.number_input("Business Assets", min_value=0.0)
rental = st.number_input("Rental Income Saved", min_value=0.0)

st.header("💳 Loans")
loans = st.number_input("Total Loans", min_value=0.0)

st.header("💳 Debts")
debts = st.number_input("Total Debts", min_value=0.0)

nisab_threshold = st.number_input("Nisab Threshold (Enter Current Value)", min_value = 0.0)

if st.button("Calculate Zakaat"):
    data = {
        "cash": cash,
        "investments": investments,
        "gold": gold,
        "silver": silver,
        "business": business,
        "rental": rental,
        "loans": loans,
        "debts": debts

    }
    
    total, zakaat = calculate_zakaat(data, nisab_threshold)

    st.subheader("📊 Results")
    st.write(f"Total Zakatable Assets: {currency} {total:.2f}")
    st.write(f"Zakaat Due: {currency} {zakaat:.2f}")

    summary = f"""
    Total assets: {total}
    Nissab Threshold: {nisab_threshold}
    Zakaat due: {zakaat}
    """

    explanation = generate_explanation(summary)

    st.subheader("🤖 AI Explanation")
    st.write(explanation)
    
    save_record({
        **data,
        "total": total,
        "nisab": nisab_threshold,
        "zakaat": zakaat,
        "currency": currency
    })