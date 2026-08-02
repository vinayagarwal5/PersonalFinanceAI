import streamlit as st


def show_metric_cards(summary):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("💰 Total Budget", f"₹{summary['total_budget']:,.0f}")

    with col2:
        st.metric("💸 Actual Spend", f"₹{summary['actual']:,.0f}")

    with col3:
        st.metric("🏦 Remaining", f"₹{summary['remaining']:,.0f}")

    with col4:
        st.metric("📊 Budget Used", f"{summary['usage']:.1f}%")
