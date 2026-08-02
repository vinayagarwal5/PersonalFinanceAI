import os
import sys
import streamlit as st

# ---------------------------------------------------------
# Add project root to Python path
# ---------------------------------------------------------

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from analytics.analytics_service import AnalyticsService
from components.kpi_cards import render_kpi_cards
from components.insight_cards import render_insights


def show_home():

    analytics = AnalyticsService()

    try:
        # =====================================================
        # HEADER
        # =====================================================

        st.title("💰 Personal Finance AI")

        st.caption("Your Personal Financial Dashboard")

        st.divider()

        # =====================================================
        # KPI SECTION
        # =====================================================

        total_spending = analytics.total_spending()
        total_income = analytics.total_income()
        net_cashflow = analytics.current_balance()
        total_transactions = analytics.total_transactions()

        render_kpi_cards(total_spending, total_income, net_cashflow, total_transactions)

        st.divider()

        # =====================================================
        # MONTHLY SPENDING
        # =====================================================

        st.subheader("📈 Monthly Spending")

        monthly_df = analytics.monthly_spending_df()

        if monthly_df.empty:
            st.info("No monthly spending available.")

        else:
            st.line_chart(monthly_df.set_index("month"))

        st.divider()

        # =====================================================
        # CATEGORY SPENDING
        # =====================================================

        st.subheader("🥧 Category Spending")

        category_df = analytics.spending_by_category()

        if category_df.empty:
            st.info("No category spending found.")

        else:
            st.dataframe(category_df, use_container_width=True, hide_index=True)

        st.divider()

        # =====================================================
        # TOP MERCHANTS
        # =====================================================

        st.subheader("🏆 Top Merchants")

        merchant_df = analytics.top_merchants()

        st.dataframe(merchant_df, use_container_width=True, hide_index=True)

        st.divider()

        # =====================================================
        # RECENT TRANSACTIONS
        # =====================================================

        st.subheader("🕒 Recent Transactions")

        recent_df = analytics.recent_transactions()

        st.dataframe(recent_df, use_container_width=True, hide_index=True)

        st.divider()

        render_insights(total_spending, total_income, category_df, merchant_df)

    finally:
        analytics.close()


if __name__ == "__main__":
    st.set_page_config(page_title="Personal Finance AI", page_icon="💰", layout="wide")

    show_home()
