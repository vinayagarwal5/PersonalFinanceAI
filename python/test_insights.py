from dashboard.components.insight_cards import render_insights
import pandas as pd
import streamlit as st

category_df = pd.DataFrame(
    {"category": ["Family", "Shopping", "Travel"], "spending": [100000, 50000, 20000]}
)

merchant_df = pd.DataFrame(
    {
        "merchant": ["Amazon", "Blinkit", "Divya Gupta"],
        "spending": [25000, 18000, 10000],
    }
)

render_insights(
    total_spending=170000,
    total_income=120000,
    category_df=category_df,
    merchant_df=merchant_df,
)
