import streamlit as st


def show_budget_table(df):

    if df.empty:
        st.info("No budgets found.")
        return

    display = df.copy()

    display["budget_amount"] = display["budget_amount"].map(lambda x: f"₹{x:,.0f}")

    display["actual"] = display["actual"].map(lambda x: f"₹{x:,.0f}")

    display["remaining"] = display["remaining"].map(lambda x: f"₹{x:,.0f}")

    display["used_percent"] = display["used_percent"].map(lambda x: f"{x:.1f}%")

    display = display.rename(
        columns={
            "category": "Category",
            "budget_amount": "Budget",
            "actual": "Actual",
            "remaining": "Remaining",
            "used_percent": "Used %",
            "status": "Status",
        }
    )

    st.dataframe(
        display,
        hide_index=True,
        use_container_width=True,
    )
