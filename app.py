import streamlit as st
from database import init_db, save_record, get_records
from calculator import calculate_zakaat
from ai_explainer import generate_explanation
from gold_silver_price import get_gold_silver_price_per_gram

init_db()

page = st.sidebar.selectbox(
    "Navigation",
    ["Zakaat Calculator", "History"]
)

nisab_method = st.selectbox(
    "Select Nisab Standard",
    ["Gold (87.48g)", "Silver (612.36g)"]
)
st.info(
"Many scholars recommend using the Silver Nisab standard because it results in a lower threshold and benefits those in need."
)

if page == "History":
    st.title("Zakaat History")
    records = get_records()
    for r in records:
        st.write(
            f"Date: {r['date']} | Total Assets: {r['total_assets']} | Zakaat Paid: {r['zakaat_due']}"
        )

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

    gold_price, silver_price = get_gold_silver_price_per_gram()
    
    total, nisab, zakaat = calculate_zakaat(
        data,
        gold_price,
        silver_price,
        nisab_method
    )

    st.subheader("📊 Results")
    st.write(f"Total Zakatable Assets: {currency} {total:.2f}")
    st.write(f"Nisab Threshold: {currency} {nisab:.2f}")
    st.write(f"Zakaat Due: {currency} {zakaat:.2f}")

    summary = f"""
    Total assets: {total}
    Nissab Threshold: {nisab}
    Zakaat due: {zakaat}
    """

    explanation = generate_explanation(summary)

    st.subheader("🤖 AI Explanation")
    st.write(explanation)
    
    save_record({
        **data,
        "total": total,
        "nisab": nisab,
        "zakaat": zakaat,
        "currency": currency
    })