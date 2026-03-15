import streamlit as st
from database.database import init_db, save_record, get_records
from services.calculator import calculate_zakat
from services.ai_explainer import generate_explanation
from utils.gold_silver_price import get_gold_silver_price_per_gram
from utils.charts import zakat_breakdown_chart, zakat_vs_assets_chart, zakat_trend, asset_breakdown
import pandas as pd
import datetime

st.set_page_config(page_title="Zakat Calculator", layout="wide")
st.title("🕌 AI Zakat Calculator")

# configuration for asset fields
ASSET_FIELDS = {
    "cash": "Bank and Cash Balance",
    "gold": "Gold Value",
    "silver": "Silver Value",
    "investments": "Crypto / Stocks",
    "business": "Business Assets",
    "rental": "Rental Savings",
    "loans": "Loans",
    "debts": "Debts"
}

init_db()

# sidebar navigation
page = st.sidebar.selectbox(
    "Navigation",
    ["Zakat Calculator", "History"]
)

st.info(
"Many scholars recommend using the Silver Nisab standard because it results in a lower threshold and benefits those in need."
)

# =============================
# ZAKAT CALCULATOR PAGE
# =============================
if page == "Zakat Calculator":

    current_year = datetime.datetime.now().year
    year = st.selectbox(
        "Select Zakat Year",
        list(range(current_year, current_year - 10, -1))
    )

    nisab_method = st.selectbox(
    "Select Nisab Standard",
    ["Gold (87.48g)", "Silver (612.36g)"]
    )

    currency = st.selectbox("Select Currency", ["USD", "CAD", "EUR", "GBP", "INR", "PKR", "AED"])

    st.header("Calculate Your Zakat")

    col1, col2, col3  = st.columns(3)

    with col1:
        st.subheader("Cash Assets")

        cash = st.number_input(
            ASSET_FIELDS["cash"],
            min_value=0.0,
            value = st.session_state.get("cash", 0.0)
        )
        gold = st.number_input(
            ASSET_FIELDS["gold"], 
            min_value=0.0,
            value = st.session_state.get("gold", 0.0)
            )
        silver = st.number_input(
            ASSET_FIELDS["silver"], 
            min_value=0.0,
            value = st.session_state.get("silver", 0.0)
            )
        
    with col2:
        st.subheader("Business/Stocks")
        investments = st.number_input(
            ASSET_FIELDS["investments"],
            min_value=0.0,
            value = st.session_state.get("investments", 0.0)
        )
        business = st.number_input(
            ASSET_FIELDS["business"],
            min_value=0.0,
            value = st.session_state.get("business", 0.0)
        )
        rental = st.number_input(
            ASSET_FIELDS["rental"],
            min_value=0.0,
            value = st.session_state.get("rental", 0.0)
        )

    with col3:
        st.subheader("Liabilities")

        loans = st.number_input(
            ASSET_FIELDS["loans"],
            min_value=0.0,
            value = st.session_state.get("loans", 0.0)
        )
        debts = st.number_input(
            ASSET_FIELDS["debts"],
            min_value=0.0,
            value = st.session_state.get("debts", 0.0)
        )


    if st.button("Calculate Zakat"):
        data = {
            "year": year,
            "cash": cash,
            "gold": gold,
            "silver": silver,
            "investments": investments,
            "business": business,
            "rental": rental,
            "loans": loans,
            "debts": debts
        }

        gold_price, silver_price = get_gold_silver_price_per_gram()
        
        total_assets, nisab_threshold, zakat_due = calculate_zakat(
            data,
            gold_price,
            silver_price,
            nisab_method
        )

        st.subheader("📊 Results")
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Assets", f"${total_assets:,.2f}")
        col2.metric("Nisab Threshold", f"${nisab_threshold:,.2f}")
        col3.metric("Zakat Due (2.5%)", f"${zakat_due:,.2f}")

        summary = f"""
        Total assets: {total_assets}
        Nissab Threshold: {nisab_threshold}
        Zakaat due: {zakat_due}
        """

        asset_data = [
            cash,
            gold,
            silver,
            investments,
            business,
            rental,
            loans,
        ]

        fig = zakat_breakdown_chart(asset_data)
        st.plotly_chart(fig,
                        config={"displayModeBar": False})

        fig2 = zakat_vs_assets_chart(total_assets, zakat_due)
        st.plotly_chart(fig2,
                        config={"displayModeBar": False})

        save_record({
            **data,
            "total_assets": total_assets,
            "nisab_threshold": nisab_threshold,
            "zakat_due": zakat_due,
            "currency": currency
        })


        explanation = generate_explanation(summary)

        st.subheader("🤖 AI Explanation")
        st.write(explanation)

# =============================
# HISTORY PAGE
# =============================
elif page == "History":
    st.title("Zakaat History")
    st.subheader("Zakat Calculation History")
    records = get_records()

    if records:
        df = pd.DataFrame(records, columns=records[0].keys())
        df = df.rename(columns={
            "year": "Year",
            "date": "Date",
            "cash": "Cash Assets",
            "gold_value": "Gold Value",
            "silver_value": "Silver Value",
            "investments": "Investments",
            "business_assets": "Business Assets",
            "rental_savings": "Rental Savings",
            "loans": "Loans",
            "debts": "Debts",
            "total_assets": "Total Assets",
            "nisab_threshold": "Nisab Threshold",
            "zakat_due": "Zakat Due",
            "currency": "Currency"
        })

        df["Year"] = df["Year"].astype(str)
        df.drop('id', axis=1, inplace=True)

        st.subheader("Historical Records")
        st.dataframe(
            df,
            width='stretch',
            hide_index=True
        )
        # CSV Download
        csv = df.to_csv(index=False)

        st.download_button(
            label="Download History as CSV",
            data=csv,
            file_name="zakat_history.csv",
            mime="text/csv"
        )
        # Detailed Records
        st.divider()
        st.subheader("Detailed Records")
        for row in records:

            title = (
                f"{row['date']} | "
                f"Total Assets: ${row['total_assets']:,.2f} | "
                f"Zakat Due: ${row['zakat_due']:,.2f}"
            )

            with st.expander(title):

                st.write("Cash Assets:", row["cash"])
                st.write("Investments:", row["investments"])
                st.write("Gold Value:", row["gold_value"])
                st.write("Silver Value:", row["silver_value"])
                st.write("Business Assets:", row["business_assets"])
                st.write("Rental Savings:", row["rental_savings"])
                st.write("Loans:", row["loans"])
                st.write("Debts:", row["debts"])
        # Chart
        st.subheader("Zakat Trend by Year")
        fig = zakat_trend(df)
        st.plotly_chart(fig,
                        config={"displayModeBar": False})
        
        st.subheader("Asset Breakdown")
        latest_record = df.iloc[0]

        cash_total = (
            latest_record["Cash Assets"] +
            latest_record["Gold Value"] +
            latest_record["Silver Value"]
        )

        investment_total = (
            latest_record["Investments"] +
            latest_record["Business Assets"] +
            latest_record["Rental Savings"]
        )

        liability_total = (
            latest_record["Loans"] -
            latest_record["Debts"]
        )

        asset_data = {
            "Category": [
                "Cash",
                "Investments",
                "Liabilities"
            ],
            "Amount": [
                cash_total, investment_total, liability_total
            ]
        }

        asset_df = pd.DataFrame(asset_data)
        fig_assets = asset_breakdown(asset_df)
        st.plotly_chart(
            fig_assets,
            config={"displayModeBar":False}
        )

    else:
        st.info("No previous records found.")