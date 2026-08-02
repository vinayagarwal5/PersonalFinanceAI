import os
import sys
import streamlit as st

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from services.cashflow_service import CashFlowService

from components.page_header import show_page_header

from components.cashflow_charts import (
    income_expense_chart,
    savings_chart,
    savings_rate_chart,
)


def show_cashflow():

    service = CashFlowService()

    try:
        show_page_header("📊 Cash Flow Dashboard", "Track Income, Expenses and Savings")

        summary = service.summary()

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Income", f"₹{summary['income']:,.0f}")

        c2.metric("Expenses", f"₹{summary['expenses']:,.0f}")

        c3.metric("Savings", f"₹{summary['savings']:,.0f}")

        c4.metric("Saving Rate", f"{summary['saving_rate']:.1f}%")

        st.divider()

        df = service.monthly_cashflow()

        if df.empty:
            st.info("No transactions found.")

            return

        st.plotly_chart(income_expense_chart(df), use_container_width=True)

        st.plotly_chart(savings_chart(df), use_container_width=True)

        st.plotly_chart(savings_rate_chart(df), use_container_width=True)

        st.subheader("Monthly Cash Flow")

        st.dataframe(df, hide_index=True, use_container_width=True)

    finally:
        service.close()


if __name__ == "__main__":
    st.set_page_config(page_title="Cash Flow", page_icon="📊", layout="wide")

    show_cashflow()
