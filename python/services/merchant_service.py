import pandas as pd

from services.database import get_connection


class MerchantService:
    @staticmethod
    def get_all_merchants():

        conn = get_connection()

        query = """
        SELECT
            merchant_name,
            normalized_name,
            category,
            sub_category,
            merchant_type,
            is_active,
            created_at,
            last_updated
        FROM merchant_master
        ORDER BY normalized_name
        """

        df = pd.read_sql(query, conn)

        conn.close()

        return df

    @staticmethod
    def search_merchants(search_text):

        conn = get_connection()

        value = f"%{search_text}%"

        query = """
        SELECT
            merchant_name,
            normalized_name,
            category,
            sub_category,
            merchant_type,
            is_active,
            created_at,
            last_updated
        FROM merchant_master
        WHERE
            merchant_name LIKE ?
            OR normalized_name LIKE ?
            OR category LIKE ?
        ORDER BY normalized_name
        """

        df = pd.read_sql(query, conn, params=(value, value, value))

        conn.close()

        return df

    @staticmethod
    def update_merchant(
        merchant_name, normalized_name, category, sub_category=None, merchant_type=None
    ):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE merchant_master
            SET
                normalized_name=?,
                category=?,
                sub_category=?,
                merchant_type=?,
                last_updated=CURRENT_TIMESTAMP
            WHERE merchant_name=?
            """,
            (normalized_name, category, sub_category, merchant_type, merchant_name),
        )

        conn.commit()
        conn.close()

    @staticmethod
    def set_active(merchant_name, active=True):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE merchant_master
            SET
                is_active=?,
                last_updated=CURRENT_TIMESTAMP
            WHERE merchant_name=?
            """,
            (1 if active else 0, merchant_name),
        )

        conn.commit()
        conn.close()

    @staticmethod
    def get_categories():

        conn = get_connection()

        query = """
        SELECT DISTINCT category
        FROM merchant_master
        ORDER BY category
        """

        df = pd.read_sql(query, conn)

        conn.close()

        return df["category"].tolist()
    @staticmethod
    def get_merchant(merchant_name):

        conn = get_connection()

        query = """
        SELECT *
        FROM merchant_master
        WHERE merchant_name=?
        """

        df = pd.read_sql(
            query,
            conn,
            params=(merchant_name,)
    )

        conn.close()

        if len(df) == 0:
            return None

        return df.iloc[0]
