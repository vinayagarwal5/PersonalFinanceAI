import plotly.express as px


def merchant_bar_chart(df):

    fig = px.bar(
        df,
        x="spending",
        y="merchant",
        orientation="h",
        text="spending",
        title="Top 10 Merchants"
    )

    fig.update_layout(
        height=450,
        yaxis=dict(categoryorder="total ascending"),
        xaxis_title="Amount (₹)",
        yaxis_title="Merchant",
        margin=dict(l=10, r=10, t=50, b=10)
    )

    fig.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside"
    )

    return fig


def category_pie_chart(df):

    fig = px.pie(
        df,
        values="spending",
        names="category",
        hole=0.35,
        title="Spending by Category"
    )

    fig.update_traces(
        textinfo="percent+label"
    )

    return fig


def source_donut_chart(df):

    fig = px.pie(
        df,
        values="spending",
        names="source",
        hole=0.60,
        title="Payment Sources"
    )

    fig.update_traces(
        textinfo="label+percent"
    )

    return fig