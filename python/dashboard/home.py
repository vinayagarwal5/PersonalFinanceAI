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


def show_home():

    analytics = AnalyticsService()

    try:

        # =====================================================
        # PAGE HEADER
        # =====================================================

        st.title("💰 Personal Finance AI")

        st.caption("Your Personal Financial Dashboard")

        st.divider()

        # =====================================================
        # KPI SECTION
        # =====================================================

        total_spending = analytics.total_spending()
        total_income = analytics.total_income()
        balance = analytics.current_balance()
        total_transactions = analytics.total_transactions()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "💸 Total Spending",
                f"₹{total_spending:,.2f}"
            )

        with col2:
            st.metric(
                "💰 Total Income",
                f"₹{total_income:,.2f}"
            )

        with col3:
            st.metric(
                "🏦 Net Balance",
                f"₹{balance:,.2f}"
            )

        with col4:
            st.metric(
                "🧾 Transactions",
                total_transactions
            )

        st.divider()

        # =====================================================
        # MONTHLY TREND
        # =====================================================

        st.subheader("📈 Monthly Spending Trend")

        monthly_df = analytics.monthly_spending_df()

        if not monthly_df.empty:

            chart_df = monthly_df.set_index("month")

            st.line_chart(chart_df)

        else:

            st.info("No monthly spending data found.")

        st.divider()

        # =====================================================
        # CATEGORY SPENDING
        # =====================================================

        st.subheader("🥧 Spending by Category")

        category_df = analytics.spending_by_category()

        if not category_df.empty:

            st.dataframe(
                category_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No category data available.")

        st.divider()

        # =====================================================
        # TOP MERCHANTS
        # =====================================================

        st.subheader("🏆 Top Merchants")

        merchant_df = analytics.top_merchants()

        st.dataframe(
            merchant_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # =====================================================
        # RECENT TRANSACTIONS
        # =====================================================

        st.subheader("🕒 Recent Transactions")

        recent_df = analytics.recent_transactions()

        st.dataframe(
            recent_df,
            use_container_width=True,
            hide_index=True
        )

    finally:

        analytics.close()


if __name__ == "__main__":

    st.set_page_config(
        page_title="Personal Finance AI",
        page_icon="💰",
        layout="wide"
    )

    show_home()