from utils.merchant_rules import MERCHANT_RULES


def get_merchant_details(merchant):

    if not merchant:
        return {
            "merchant": "Unknown",
            "category": "Others"
        }

    merchant = merchant.strip()
    merchant_upper = merchant.upper()

    for keyword, (normalized, category) in MERCHANT_RULES.items():

        if keyword.upper() in merchant_upper:
            return {
                "merchant": normalized,
                "category": category
            }

    return {
        "merchant": merchant.title(),
        "category": "Others"
    }