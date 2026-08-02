import streamlit as st


def render_insights(total_spending, total_income, category_df, merchant_df):
    """
    Render Finance Insights
    """

    st.subheader("💡 Financial Insights")

    insights = []

    # -------------------------------------------------------
    # Spending vs Income
    # -------------------------------------------------------

    if total_income > 0:
        ratio = (total_spending / total_income) * 100

        insights.append(f"💸 Spending is **{ratio:.1f}%** of recorded income.")

    # -------------------------------------------------------
    # Largest Category
    # -------------------------------------------------------

    if not category_df.empty:
        top_category = category_df.iloc[0]

        insights.append(
            f"📂 Highest spending category is **{top_category['category']}** "
            f"(₹{top_category['spending']:,.2f})."
        )

    # -------------------------------------------------------
    # Largest Merchant
    # -------------------------------------------------------

    if not merchant_df.empty:
        top_merchant = merchant_df.iloc[0]

        insights.append(
            f"🏪 Top merchant is **{top_merchant['merchant']}** "
            f"(₹{top_merchant['spending']:,.2f})."
        )

    # -------------------------------------------------------
    # Low Income Warning
    # -------------------------------------------------------

    if total_income < total_spending:
        insights.append(
            "⚠️ Recorded spending exceeds recorded income. "
            "This may indicate missing income transactions."
        )

    # -------------------------------------------------------
    # Display
    # -------------------------------------------------------

    for item in insights:
        st.info(item)
