import re
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

try:
    from .base_parser import BasePDFParser
    from ..services.database import insert_transaction
    from ..services.merchant_normalizer import get_merchant_details
    from ..utils.date_utils import (
        convert_date,
        get_month,
        get_financial_year
    )
    from ..utils.constants import (
        ICICI,
        ICICI_DATE_FORMAT,
        PAYMENT_MODE_CC
    )
except ImportError:
    # Support direct script execution from the python/parsers folder.
    sys.path.append(str(Path(__file__).resolve().parent.parent))

    from parsers.base_parser import BasePDFParser
    from services.database import insert_transaction
    from utils.merchant_utils import clean_merchant_name
    from services.merchant_normalizer import get_merchant_details
    from utils.date_utils import (
        convert_date,
        get_month,
        get_financial_year
    )
    from utils.constants import (
        ICICI,
        ICICI_DATE_FORMAT,
        PAYMENT_MODE_CC
    )

class ICICIParser(BasePDFParser):

    def __init__(self):

        pdf_file = (
            Path(__file__).parent.parent.parent
            / "data"
            / "incoming"
            / "Icici_cc.pdf"
        )

        super().__init__(pdf_file, ICICI)

    def run(self):

        if self.is_file_processed():
            return

        text = self.extract_text()

        text = text.replace("\n", " ")
        text = re.sub(r"\s+", " ", text)

        pattern = re.compile(
            r'(\d{2}-[A-Z]{3}-\d{2})\s+'
            r'([A-Z0-9]+)\s+'
            r'(.*?)\s+'
            r'0\.00\s+'
            r'(-?[\d,]+\.\d{2})'
        )

        matches = list(pattern.finditer(text))

        for match in matches:

            description = match.group(3)

            merchant = clean_merchant_name(description)

            details = get_merchant_details(merchant)

            amount = float(match.group(4).replace(",", ""))

            transaction = {

                "transaction_date": convert_date(
                    match.group(1),
                    ICICI_DATE_FORMAT
                ),

                "transaction_time": None,

                "month": get_month(
                    match.group(1),
                    ICICI_DATE_FORMAT
                ),

                "financial_year": get_financial_year(
                    match.group(1),
                    ICICI_DATE_FORMAT
                ),

                "merchant": details["merchant"],

                "description": description,

                "amount": abs(amount),

                "transaction_type": (
                    "Credit"
                    if amount < 0
                    else "Debit"
                ),

                "payment_mode": PAYMENT_MODE_CC,

                "source": ICICI,

                "account": "4315XXXX7001",

                "reference_no": match.group(2),

                "category": details["category"],

                "raw_text": match.group(0)

            }

            if insert_transaction(transaction):
                self.inserted += 1
            else:
                self.duplicates += 1

        self.mark_completed()

        self.print_summary(len(matches))


if __name__ == "__main__":

    ICICIParser().run()