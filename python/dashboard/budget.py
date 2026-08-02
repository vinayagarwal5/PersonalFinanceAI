import os
import sys

import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# Add project root
# ---------------------------------------------------------

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from services.budget_service import BudgetService


def show_budget():

    budget_service = BudgetService()

    try:
        st.title("💰 Budget Planner")

        st.caption("Set monthly budgets and track actual spending")

        st.divider()

        # -------------------------------------------------
        # Budget Entry
        # -------------------------------------------------

        st.subheader("➕ Add / Update Budget")

        categories = budget_service.get_categories()

        month = st.selectbox(
            "Month",
            sorted(
                pd.date_range("2026-01-01", periods=24, freq="MS").strftime("%Y-%m"),
                reverse=True,
            ),
        )

        category = st.selectbox("Category", categories)

        amount = st.number_input(
            "Budget Amount (₹)", min_value=0.0, step=500.0, format="%.2f"
        )

        if st.button("💾 Save Budget"):
            budget_service.save_budget(month, category, amount)

            st.success("Budget saved successfully.")

            st.rerun()

        st.divider()

        # -------------------------------------------------
        # Budget Overview
        # -------------------------------------------------

        st.subheader("📊 Budget vs Actual")

        selected_month = st.selectbox(
            "View Month",
            sorted(
                pd.date_range("2026-01-01", periods=24, freq="MS").strftime("%Y-%m"),
                reverse=True,
            ),
            key="view_month",
        )

        df = budget_service.budget_vs_actual(selected_month)

        if df.empty:
            st.info("No budgets created for this month.")

            return

        # -------------------------------------------------
        # Progress
        # -------------------------------------------------

        for _, row in df.iterrows():
            budget = float(row["budget_amount"])
            actual = float(row["actual"])
            remaining = float(row["remaining"])

            percent = 0 if budget == 0 else actual / budget

            if percent < 0.8:
                status = "🟢 Within Budget"

            elif percent <= 1:
                status = "🟡 Near Limit"

            else:
                status = "🔴 Over Budget"

            st.markdown(f"### {row['category']}")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Budget", f"₹{budget:,.0f}")

            col2.metric("Actual", f"₹{actual:,.0f}")

            col3.metric("Remaining", f"₹{remaining:,.0f}")

            col4.metric("Status", status)

            st.progress(min(percent, 1.0))

            st.divider()

    finally:
        budget_service.close()


if __name__ == "__main__":
    st.set_page_config(page_title="Budget Planner", page_icon="💰", layout="wide")

    show_budget()
