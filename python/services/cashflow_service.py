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
                    WHEN transaction_type='Expense'
                    THEN amount
                    ELSE 0
                END
            ) AS expenses,

            SUM(
                CASE
                    WHEN transaction_type='Income'
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

        df["savings"] = df["income"] - df["expenses"]

        df["saving_rate"] = (df["savings"] / df["income"] * 100).fillna(0).round(2)

        return df

    # ---------------------------------------------------------
    # Monthly Summary
    # ---------------------------------------------------------

    def summary(self):

        df = self.monthly_cashflow()

        if df.empty:
            return {"income": 0, "expenses": 0, "savings": 0, "saving_rate": 0}

        latest = df.iloc[-1]

        return {
            "income": latest["income"],
            "expenses": latest["expenses"],
            "savings": latest["savings"],
            "saving_rate": latest["saving_rate"],
        }

    # ---------------------------------------------------------
    # Close
    # ---------------------------------------------------------

    def close(self):

        self.conn.close()
