import re


def clean_phonepe(desc):

    desc = desc.replace("Paid to ", "")
    desc = desc.replace("Received from ", "")
    desc = desc.replace("Collect request from ", "")
    desc = desc.replace("Payment to ", "")

    desc = re.sub(r"\s+", " ", desc)

    return desc.strip()


def clean_merchant_name(desc):

    if not desc:
        return "Unknown"

    desc = desc.strip()

    # Remove repeated spaces
    desc = re.sub(r"\s+", " ", desc)

    # Remove common ICICI banking text
    patterns = [
        r"Debit Inr.*",
        r"Credit Inr.*",
        r"Transaction Id.*",
        r"Bank Account.*",
        r"UPI Ref.*",
        r"UPI/.*",
    ]

    for pattern in patterns:
        desc = re.sub(pattern, "", desc, flags=re.IGNORECASE)

    return desc.strip(" -")
