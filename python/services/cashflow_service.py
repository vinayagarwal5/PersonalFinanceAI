from services.base_service import BaseService
import pandas as pd


class CashFlowService(BaseService):
    # ---------------------------------------------------------
    # Monthly Cash Flow
    # ---------------------------------------------------------

    def monthly_cashflow(self):

        query = """
        SELECT

            month,

            SUM(
                CASE
                    WHEN transaction_type='Debit'
                    THEN amount
                    ELSE 0
                END
            ) AS expenses,

            SUM(
                CASE
                    WHEN transaction_type='Credit'
                    THEN amount
                    ELSE 0
                END
            ) AS income

        FROM transactions

        GROUP BY month

        ORDER BY month
        """

        df = pd.read_sql_query(query, self.conn)

        if df.empty:
            return df

        df["expenses"] = df["expenses"].fillna(0)

        df["income"] = df["income"].fillna(0)

        df["savings"] = df["income"] - df["expenses"]

        df["saving_rate"] = (
            ((df["savings"] / df["income"].replace(0, pd.NA)) * 100).fillna(0).round(2)
        )

        return df

    # ---------------------------------------------------------
    # Latest Month Summary
    # ---------------------------------------------------------

    def summary(self):

        df = self.monthly_cashflow()

        if df.empty:
            return {
                "income": 0,
                "expenses": 0,
                "savings": 0,
                "saving_rate": 0,
            }

        latest = df.sort_values("month").iloc[-1]

        return {
            "income": float(latest["income"]),
            "expenses": float(latest["expenses"]),
            "savings": float(latest["savings"]),
            "saving_rate": float(latest["saving_rate"]),
        }

    # ---------------------------------------------------------
    # Close
    # ---------------------------------------------------------

    def close(self):

        self.conn.close()
