import plotly.express as px
import pandas as pd 

def zakaat_breakdown_chart(data):

    df = pd.DataFrame({
        "Category": [
            "Cash",
            "Gold/Silver",
            "Stocks/Crypto",
            "Loans",
            "Property/Business"
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