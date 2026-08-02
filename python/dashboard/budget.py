import os
import sys

import streamlit as st

# ---------------------------------------------------------
# Add Project Root
# ---------------------------------------------------------

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

from services.budget_service import BudgetService

from components.page_header import show_page_header
from components.metric_cards import show_metric_cards
from components.budget_table import show_budget_table
from components.progress_cards import show_progress


# ---------------------------------------------------------
# Budget Page
# ---------------------------------------------------------


def show_budget():

    budget_service = BudgetService()

    try:
        # =====================================================
        # PAGE HEADER
        # =====================================================

        show_page_header(
            "💰 Budget Planner",
            "Plan your monthly spending and monitor budget performance",
        )

        # =====================================================
        # MONTH SELECTOR
        # =====================================================

        months = budget_service.get_months()

        if not months:
            st.warning("No transaction months found.")

            return

        selected_month = st.selectbox("Select Month", months, index=0)

        # =====================================================
        # SUMMARY
        # =====================================================

        summary = budget_service.budget_summary(selected_month)

        show_metric_cards(summary)

        st.divider()

        # =====================================================
        # ADD / UPDATE BUDGET
        # =====================================================

        st.subheader("➕ Add / Update Budget")

        categories = budget_service.get_categories()

        with st.form("budget_form"):
            category = st.selectbox("Category", categories)

            amount = st.number_input(
                "Budget Amount (₹)", min_value=0.0, step=500.0, format="%.2f"
            )

            submitted = st.form_submit_button("💾 Save Budget")

            if submitted:
                budget_service.save_budget(selected_month, category, amount)

                st.success(f"Budget saved for {category}")

                st.rerun()

        st.divider()

        # =====================================================
        # BUDGET DATA
        # =====================================================

        budget_df = budget_service.budget_vs_actual(selected_month)

        if budget_df.empty:
            st.info("No budgets configured for this month.")

            return
            # =====================================================
        # BUDGET SUMMARY TABLE
        # =====================================================

        edited_df = show_budget_table(budget_df)

        st.divider()

        # =====================================================
        # PROGRESS SECTION
        # =====================================================

        show_progress(budget_df)

        st.divider()

        # =====================================================
        # DELETE BUDGET
        # =====================================================

        st.subheader("🗑 Delete Budget")

        delete_category = st.selectbox(
            "Select Category", budget_df["category"].tolist(), key="delete_category"
        )

        if st.button("Delete Budget", type="secondary"):
            budget_service.delete_budget(selected_month, delete_category)

            st.success(f"{delete_category} budget deleted.")

            st.rerun()

        st.divider()

        # =====================================================
        # BUDGET STATISTICS
        # =====================================================

        st.subheader("📌 Budget Statistics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Categories", len(budget_df))

        with col2:
            within_budget = len(budget_df[budget_df["status"] == "🟢 Within Budget"])

            st.metric("Within Budget", within_budget)

        with col3:
            over_budget = len(budget_df[budget_df["status"] == "🔴 Over Budget"])

            st.metric("Over Budget", over_budget)

    finally:
        budget_service.close()


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":
    st.set_page_config(page_title="Budget Planner", page_icon="💰", layout="wide")

    show_budget()
