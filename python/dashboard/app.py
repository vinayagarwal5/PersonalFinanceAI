import os
import sys

import streamlit as st
import plotly.express as px

# ---------------------------------------------------------
# Add project root to Python path
# ---------------------------------------------------------
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.append(PROJECT_ROOT)

from analytics.analytics_service import AnalyticsService

from dashboard.charts import (
    merchant_bar_chart,
    category_pie_chart,
    source_donut_chart
)

# ---------------------------------------------------------
# Page Config
# ---------------------------------------------------------
st.set_page_config(
    page_title="Personal Finance Dashboard",
    page_icon="💰",
    layout="wide"
)

analytics = AnalyticsService()

# ---------------------------------------------------------
# Title
# ---------------------------------------------------------
st.title("💰 Personal Finance Dashboard")
st.markdown("---")

# ---------------------------------------------------------
# KPI Section
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💸 Total Spending",
        f"₹{analytics.total_spending():,.2f}"
    )

with col2:
    st.metric(
        "💰 Total Income",
        f"₹{analytics.total_income():,.2f}"
    )

with col3:
    st.metric(
        "📄 Transactions",
        analytics.total_transactions()
    )

with col4:
    st.metric(
        "📊 Avg Transaction",
        f"₹{analytics.average_transaction():,.2f}"
    )

st.markdown("---")

# ---------------------------------------------------------
# Monthly Spending Trend
# ---------------------------------------------------------
st.subheader("📈 Monthly Spending Trend")

monthly_df = analytics.monthly_spending_df()

if not monthly_df.empty:

    fig = px.line(
        monthly_df,
        x="month",
        y="spending",
        markers=True,
        title="Monthly Spending"
    )

    fig.update_layout(
        height=450,
        xaxis_title="Month",
        yaxis_title="Amount (₹)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.info("No monthly spending data found.")

st.markdown("---")

# ---------------------------------------------------------
# Category & Source Charts
# ---------------------------------------------------------
left_col, right_col = st.columns(2)

with left_col:

    st.subheader("🥧 Spending by Category")

    category_df = analytics.spending_by_category()

    if not category_df.empty:

        fig = category_pie_chart(category_df)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("No category data available.")

with right_col:

    st.subheader("💳 Payment Sources")

    source_df = analytics.spending_by_source()

    if not source_df.empty:

        fig = source_donut_chart(source_df)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("No source data available.")

st.markdown("---")

# ---------------------------------------------------------
# Top Merchants
# ---------------------------------------------------------
st.subheader("🏪 Top 10 Merchants")

merchant_df = analytics.top_merchants()

if not merchant_df.empty:

    fig = merchant_bar_chart(merchant_df)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:
    st.info("No merchant data available.")

st.markdown("---")

# ---------------------------------------------------------
# Recent Transactions
# ---------------------------------------------------------
st.subheader("📋 Recent Transactions")

recent_df = analytics.recent_transactions()

if not recent_df.empty:

    st.dataframe(
        recent_df,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No transactions found.")

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.caption("🚀 Personal Finance AI Dashboard")

analytics.close()