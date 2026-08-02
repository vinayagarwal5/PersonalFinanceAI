import plotly.express as px


def income_expense_chart(df):

    fig = px.line(
        df,
        x="month",
        y=["income", "expenses"],
        markers=True,
        title="Income vs Expenses",
    )

    fig.update_layout(
        height=450, xaxis_title="Month", yaxis_title="Amount (₹)", legend_title=""
    )

    return fig


def savings_chart(df):

    fig = px.bar(df, x="month", y="savings", text="savings", title="Monthly Savings")

    fig.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")

    fig.update_layout(height=450, xaxis_title="Month", yaxis_title="Savings (₹)")

    return fig


def savings_rate_chart(df):

    fig = px.line(df, x="month", y="saving_rate", markers=True, title="Savings Rate")

    fig.update_layout(height=450, xaxis_title="Month", yaxis_title="Savings Rate (%)")

    return fig
