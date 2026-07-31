from utils.category_rules import CATEGORY_RULES


def categorize(merchant):

    merchant_upper = merchant.upper()

    for keyword, category in CATEGORY_RULES.items():

        if keyword.upper() in merchant_upper:

            return category

    return "Others"