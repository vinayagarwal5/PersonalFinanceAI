import pandas as pd

from services.analytics_service import AnalyticsService


class InsightsService:

    def __init__(self):
        self.analytics = AnalyticsService()

    def monthly_summary(self):

        df = self.analytics.monthly_spending_df()

        if len(df) < 2:
            return "Not enough data."

        current = df.iloc[-1]
        previous = df.iloc[-2]

        diff = current["spending"] - previous["spending"]

        if previous["spending"] > 0:
            pct = (diff / previous["spending"]) * 100
        else:
            pct = 0

        if diff >= 0:
            trend = "increased"
        else:
            trend = "decreased"

        return (
            f"Spending {trend} by ₹{abs(diff):,.2f} "
            f"({abs(pct):.1f}%) compared to last month."
        )

    def top_category(self):

        df = self.analytics.spending_by_category()

        if df.empty:
            return "No category data."

        row = df.iloc[0]

        return (
            f"Largest expense category: "
            f"{row['category']} (₹{row['spending']:,.2f})"
        )

    def top_merchant(self):

        df = self.analytics.top_merchants(limit=1)

        if df.empty:
            return "No merchant data."

        row = df.iloc[0]

        return (
            f"Top merchant: {row['merchant']} "
            f"(₹{row['spending']:,.2f})"
        )

    def biggest_transaction(self):

        query = """
        SELECT
            merchant,
            amount,
            transaction_date
        FROM transactions
        WHERE transaction_type='Debit'
        ORDER BY amount DESC
        LIMIT 1
        """

        df = pd.read_sql_query(
            query,
            self.analytics.conn
        )

        if df.empty:
            return "No transaction data."

        row = df.iloc[0]

        return (
            f"Highest expense: {row['merchant']} "
            f"(₹{row['amount']:,.2f}) "
            f"on {row['transaction_date']}"
        )

    def generate_insights(self):

        return [
            self.monthly_summary(),
            self.top_category(),
            self.top_merchant(),
            self.biggest_transaction()
        ]