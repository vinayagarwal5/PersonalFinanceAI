from database import (
    insert_transaction,
    get_transaction_count,
    transaction_exists
)

transaction = {

    "transaction_date": "2025-05-10",
    "transaction_time": "07:09 AM",
    "description": "Blinkit",

    "amount": 559,

    "transaction_type": "Debit",

    "source": "PhonePe",

    "account": "XX6399",

    "reference_no": "TEST12345",

    "category": "Groceries",

    "financial_year": "2025-26",

    "month": "May",

    "raw_text": "Sample"

}

inserted = insert_transaction(transaction)

print()

print("Inserted :", inserted)

print("Exists :", transaction_exists("PhonePe", "TEST12345"))

print("Total :", get_transaction_count())