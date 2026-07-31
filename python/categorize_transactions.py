from services.database import (
    get_uncategorized_transactions,
    update_category
)

from services.categorizer import categorize

rows = get_uncategorized_transactions()

updated = 0

for transaction_id, merchant in rows:

    category = categorize(merchant)

    update_category(
        transaction_id,
        category
    )

    updated += 1

print(f"Updated {updated} transactions.")