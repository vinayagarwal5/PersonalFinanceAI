import streamlit as st


def show_progress(df):

    if df.empty:
        st.info("No budget data available.")
        return

    st.subheader("📈 Budget Usage")

    for _, row in df.iterrows():
        st.write(f"**{row['category']}**")

        # Progress is now calculated by BudgetService
        st.progress(float(row["progress"]))

        st.caption(
            f"₹{row['actual']:,.0f} of ₹{row['budget_amount']:,.0f} "
            f"({row['used_percent']:.1f}%)"
        )

        st.write("")
