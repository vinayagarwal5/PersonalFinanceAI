import streamlit as st
import pandas as pd


def show_budget_table(df):
    """
    Displays the monthly budget table.

    Returns:
        Edited dataframe (future use)
    """

    st.subheader("📋 Monthly Budget")

    if df.empty:
        st.info("No budgets available for this month.")
        return None

    display = df.copy()

    # -------------------------------
    # Format values
    # -------------------------------

    display["Budget"] = display["budget_amount"].round(2)
    display["Actual"] = display["actual"].round(2)
    display["Remaining"] = display["remaining"].round(2)
    display["Used %"] = display["used_percent"].round(2)

    display = display[
        [
            "category",
            "Budget",
            "Actual",
            "Remaining",
            "Used %",
            "status",
        ]
    ]

    display.rename(
        columns={
            "category": "Category",
            "status": "Status",
        },
        inplace=True,
    )

    edited_df = st.data_editor(
        display,
        hide_index=True,
        use_container_width=True,
        disabled=[
            "Category",
            "Actual",
            "Remaining",
            "Used %",
            "Status",
        ],
        column_config={
            "Budget": st.column_config.NumberColumn(
                "Budget (₹)",
                min_value=0,
                step=500,
                format="₹ %.0f",
            ),
            "Actual": st.column_config.NumberColumn(
                "Actual (₹)",
                format="₹ %.0f",
            ),
            "Remaining": st.column_config.NumberColumn(
                "Remaining (₹)",
                format="₹ %.0f",
            ),
            "Used %": st.column_config.ProgressColumn(
                "Used %",
                min_value=0,
                max_value=100,
                format="%.1f%%",
            ),
        },
    )

    return edited_df
