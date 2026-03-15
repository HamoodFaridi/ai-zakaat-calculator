import plotly.express as px
import plotly.graph_objects as go
import pandas as pd 

def zakat_breakdown_chart(data):

    df = pd.DataFrame({
        "Category": [
            "Cash",
            "Gold",
            "Silver",
            "Stocks/Crypto",
            "Property/Business",
            "Rentals",
            "Loans"
        ],
        "Value": data
    })

    fig = px.pie(
        df,
        values = "Value",
        names = "Category",
        title = "Asset Breakdown"
    )

    return fig

def zakat_vs_assets_chart(total_assets, zakat_due):

    fig = go.Figure()

    fig.add_bar(
        x = ["Total Assets"],
        y = [total_assets],
        name = "Assets"
    )

    fig.add_bar(
        x = ["Zakaat Due"],
        y = [zakat_due],
        name = "Zakat"
    )

    fig.update_layout(title="Assets vs Zakat")

    return fig

def zakat_trend(data):
    fig = px.line(
        data,
        x="Year",
        y="Zakat Due",
        markers=True
    )

    fig.update_xaxes(type="category")

    return fig

def asset_breakdown(data):
    fig_assets = px.pie(
        data,
        values = "Amount",
        names = "Category",
        title = "Asset Distribution"
    )

    return fig_assets