from services.database import get_connection
from utils.merchant_rules import MERCHANT_RULES


def get_merchant_details(merchant):

    if not merchant:
        return {"merchant": "Unknown", "category": "Others"}

    merchant = merchant.strip()
    merchant_upper = merchant.upper()

    # =====================================================
    # 1. Lookup Merchant Master (SQLite)
    # =====================================================

    conn = get_connection()
    cursor = conn.cursor()

    # Detect which key column exists in merchant_master
    try:
        cursor.execute("PRAGMA table_info(merchant_master)")
        cols = [row[1] for row in cursor.fetchall()]
    except Exception:
        cols = []

    if 'keyword' in cols:
        key_col = 'keyword'
    elif 'merchant_name' in cols:
        key_col = 'merchant_name'
    else:
        key_col = None

    row = None
    if key_col:
        try:
            query = f"SELECT normalized_name, category FROM merchant_master WHERE UPPER({key_col})=?"
            cursor.execute(query, (merchant_upper,))
            row = cursor.fetchone()
        except Exception:
            row = None

    conn.close()

    if row:
        return {"merchant": row[0], "category": row[1]}

    # =====================================================
    # 2. Fallback to MERCHANT_RULES
    # =====================================================

    for keyword, (normalized, category) in MERCHANT_RULES.items():
        if keyword.upper() in merchant_upper:
            return {"merchant": normalized, "category": category}

    # =====================================================
    # 3. Unknown Merchant
    # =====================================================

    return {"merchant": merchant.title(), "category": "Others"}
