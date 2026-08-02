import streamlit as st


def render_kpi_cards(
    total_spending: float,
    total_income: float,
    net_cashflow: float,
    total_transactions: int,
):
    """
    Render Dashboard KPI Cards
    """

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("💸 Total Spending", f"₹{total_spending:,.2f}")

    with col2:
        st.metric("💰 Total Income", f"₹{total_income:,.2f}")

    with col3:
        st.metric("📊 Net Cash Flow", f"₹{net_cashflow:,.2f}")

    with col4:
        st.metric("🧾 Transactions", f"{total_transactions:,}")
