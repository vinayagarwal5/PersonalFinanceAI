import pandas as pd
try:
    from ..services.database import get_connection
except Exception:
    # Support direct execution/import when package context is not available
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    from services.database import get_connection


class AnalyticsService:
    def __init__(self):
        self.conn = get_connection()

    def close(self):
        self.conn.close()

    # =====================================================
    # KPI SECTION
    # =====================================================

    def total_spending(self):

        query = """
        SELECT IFNULL(SUM(amount),0)
        FROM transactions
        WHERE transaction_type='Debit'
        """

        return self.conn.execute(query).fetchone()[0]

    def total_income(self):

        query = """
        SELECT IFNULL(SUM(amount),0)
        FROM transactions
        WHERE transaction_type='Credit'
        """

        return self.conn.execute(query).fetchone()[0]

    def total_transactions(self):

        query = """
        SELECT COUNT(*)
        FROM transactions
        """

        return self.conn.execute(query).fetchone()[0]

    def average_transaction(self):

        query = """
        SELECT AVG(amount)
        FROM transactions
        WHERE transaction_type='Debit'
        """

        value = self.conn.execute(query).fetchone()[0]

        return round(value or 0, 2)

    def current_balance(self):

        return round(self.total_income() - self.total_spending(), 2)

    # =====================================================
    # MONTHLY SPENDING
    # =====================================================

    def monthly_spending_df(self):

        query = """
        SELECT
            month,
            ROUND(SUM(amount),2) AS spending
        FROM transactions
        WHERE transaction_type='Debit'
        GROUP BY month
        ORDER BY month
        """

        return pd.read_sql_query(query, self.conn)

    # =====================================================
    # CATEGORY
    # =====================================================

    def spending_by_category(self):

        query = """
        SELECT
            category,
            ROUND(SUM(amount),2) AS spending
        FROM transactions
        WHERE transaction_type='Debit'
        GROUP BY category
        ORDER BY spending DESC
        """

        return pd.read_sql_query(query, self.conn)

    # =====================================================
    # SOURCE
    # =====================================================

    def spending_by_source(self):

        query = """
        SELECT
            source,
            ROUND(SUM(amount),2) AS spending
        FROM transactions
        WHERE transaction_type='Debit'
        GROUP BY source
        ORDER BY spending DESC
        """

        return pd.read_sql_query(query, self.conn)

    # =====================================================
    # TOP MERCHANTS
    # =====================================================

    def top_merchants(self, limit=10):

        query = """
        SELECT
            merchant,
            COUNT(*) AS transactions,
            ROUND(SUM(amount),2) AS spending
        FROM transactions
        WHERE transaction_type='Debit'
        GROUP BY merchant
        ORDER BY spending DESC
        LIMIT ?
        """

        return pd.read_sql_query(query, self.conn, params=(limit,))

    # =====================================================
    # RECENT TRANSACTIONS
    # =====================================================

    def recent_transactions(self, limit=20):

        query = """
        SELECT
            transaction_date,
            merchant,
            category,
            amount,
            source
        FROM transactions
        ORDER BY transaction_date DESC
        LIMIT ?
        """

        return pd.read_sql_query(query, self.conn, params=(limit,))
