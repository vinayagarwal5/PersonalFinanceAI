from services.database import (
    get_all_merchants,
    update_merchant
)

from services.merchant_normalizer import normalize_merchant

merchants = get_all_merchants()

updated = 0

for merchant in merchants:

    normalized = normalize_merchant(merchant)

    if merchant != normalized:

        print(f"{merchant}  --->  {normalized}")

        update_merchant(merchant, normalized)

        updated += 1

print()
print("=" * 60)
print(f"Merchants Updated : {updated}")