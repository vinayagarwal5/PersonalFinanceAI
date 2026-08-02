import pandas as pd

from services.base_service import BaseService


class BudgetService(BaseService):
    def __init__(self):
        super().__init__()

    # ---------------------------------------------------------
    # Available Months
    # ---------------------------------------------------------

    def get_months(self):

        query = """
        SELECT DISTINCT month
        FROM transactions
        WHERE month IS NOT NULL
        ORDER BY month DESC
        """

        df = pd.read_sql_query(query, self.conn)

        return df["month"].tolist()

    # ---------------------------------------------------------
    # Categories
    # ---------------------------------------------------------

    def get_categories(self):

        query = """
        SELECT DISTINCT category
        FROM transactions
        WHERE category IS NOT NULL
        ORDER BY category
        """

        df = pd.read_sql_query(query, self.conn)

        return df["category"].tolist()

    # ---------------------------------------------------------
    # Save Budget
    # ---------------------------------------------------------

    def save_budget(self, month, category, amount):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO budgets
            (
                month,
                category,
                budget_amount
            )
            VALUES (?,?,?)

            ON CONFLICT(month, category)
            DO UPDATE SET
                budget_amount = excluded.budget_amount
            """,
            (
                month,
                category,
                amount,
            ),
        )

        self.conn.commit()

    # ---------------------------------------------------------
    # Delete Budget
    # ---------------------------------------------------------

    def delete_budget(self, month, category):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            DELETE FROM budgets
            WHERE month=?
            AND category=?
            """,
            (
                month,
                category,
            ),
        )

        self.conn.commit()
    # ---------------------------------------------------------
    # Get Budget
    # ---------------------------------------------------------

    def get_budget(self, month, category):

        query = """
        SELECT *
        FROM budgets
        WHERE month=?
        AND category=?
        """

        df = pd.read_sql_query(
            query,
            self.conn,
            params=(month, category)
        )

        if df.empty:
            return None

        return df.iloc[0]
    # ---------------------------------------------------------
    # Budget Exists
    # ---------------------------------------------------------

    def budget_exists(self, month, category):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM budgets
            WHERE month=?
            AND category=?
            """,
            (month, category)
        )

        return cursor.fetchone()[0] > 0
    # ---------------------------------------------------------
    # Budget List
    # ---------------------------------------------------------

    def get_budgets(self, month=None):

        if month:
            query = """
            SELECT
                month,
                category,
                budget_amount
            FROM budgets
            WHERE month=?
            ORDER BY category
            """

            return pd.read_sql_query(
                query,
                self.conn,
                params=(month,),
            )

        query = """
        SELECT
            month,
            category,
            budget_amount
        FROM budgets
        ORDER BY month DESC, category
        """

        return pd.read_sql_query(query, self.conn)

    # ---------------------------------------------------------
    # Budget Summary
    # ---------------------------------------------------------

    def budget_summary(self, month):

        query = """
        SELECT
            COALESCE(SUM(budget_amount),0)
        FROM budgets
        WHERE month=?
        """

        cursor = self.conn.cursor()

        cursor.execute(query, (month,))

        total_budget = cursor.fetchone()[0] or 0

        query = """
        SELECT
            COALESCE(SUM(t.amount),0)
        FROM transactions t
        JOIN budgets b
            ON b.category=t.category
           AND b.month=t.month
        WHERE b.month=?
        """

        cursor.execute(query, (month,))

        actual = cursor.fetchone()[0] or 0

        remaining = total_budget - actual

        usage = 0

        if total_budget > 0:
            usage = round((actual / total_budget) * 100, 2)

        return {
            "total_budget": total_budget,
            "actual": actual,
            "remaining": remaining,
            "usage": usage,
        }

    # ---------------------------------------------------------
    # Budget vs Actual
    # ---------------------------------------------------------

    def budget_vs_actual(self, month):

        query = """
        SELECT

            b.category,

            b.budget_amount,

            COALESCE(SUM(t.amount),0) AS actual

        FROM budgets b

        LEFT JOIN transactions t

            ON b.category=t.category
           AND b.month=t.month

        WHERE b.month=?

        GROUP BY
            b.category,
            b.budget_amount

        ORDER BY
            b.category
        """

        df = pd.read_sql_query(
            query,
            self.conn,
            params=(month,),
        )

        if df.empty:
            return df

        df["remaining"] = df["budget_amount"] - df["actual"]

        df["used_percent"] = ((df["actual"] / df["budget_amount"]) * 100).round(2)
        df["progress"] = (df["used_percent"] / 100).clip(upper=1.0)
        
        def get_status(x):

            if x < 80:
                return "🟢 Within Budget"

            if x <= 100:
                return "🟡 Near Limit"

            return "🔴 Over Budget"

        df["status"] = df["used_percent"].apply(get_status)

        return df
