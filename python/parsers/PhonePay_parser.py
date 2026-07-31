import re
from pathlib import Path
import sys

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
        PHONEPE,
        PHONEPE_DATE_FORMAT,
        PAYMENT_MODE_UPI
    )
except ImportError:
    sys.path.append(str(Path(__file__).resolve().parent.parent))

    from parsers.base_parser import BasePDFParser
    from services.database import insert_transaction
    from services.merchant_normalizer import get_merchant_details
    from utils.date_utils import (
        convert_date,
        get_month,
        get_financial_year
    )
    from utils.constants import (
        PHONEPE,
        PHONEPE_DATE_FORMAT,
        PAYMENT_MODE_UPI
    )


class PhonePeParser(BasePDFParser):

    def __init__(self):

        pdf_file = (
            Path(__file__).parent.parent.parent
            / "data"
            / "incoming"
            / "PhonePe.pdf"
        )

        super().__init__(pdf_file, PHONEPE)

    def run(self):

        if self.is_file_processed():
            return

        text = self.extract_text()

        text = text.replace("\n", " ")
        text = re.sub(r"\s+", " ", text)

        pattern = re.compile(
            r'([A-Za-z]{3}\s+\d{2},\s+\d{4})\s+'
            r'(.*?)\s+'
            r'(Debit|Credit)\s+INR\s+([\d,]+\.\d{2})\s+'
            r'(\d{2}:\d{2}\s(?:AM|PM))\s+'
            r'Transaction ID\s*:\s*([A-Z0-9]+)\s+'
            r'UTR No\s*:\s*(\d+)\s+'
            r'(?:Debited|Credited)\s+(?:from|to)\s+([A-Z0-9]+)'
        )

        matches = list(pattern.finditer(text))

        for match in matches:

            description = match.group(2)

            details = get_merchant_details(description)

            transaction = {

                "transaction_date": convert_date(
                    match.group(1),
                    PHONEPE_DATE_FORMAT
                ),

                "transaction_time": match.group(5),

                "month": get_month(
                    match.group(1),
                    PHONEPE_DATE_FORMAT
                ),

                "financial_year": get_financial_year(
                    match.group(1),
                    PHONEPE_DATE_FORMAT
                ),

                "merchant": details["merchant"],

                "description": description,

                "amount": float(
                    match.group(4).replace(",", "")
                ),

                "transaction_type": match.group(3),

                "payment_mode": PAYMENT_MODE_UPI,

                "source": PHONEPE,

                "account": match.group(8),

                "reference_no": match.group(7),

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

    PhonePeParser().run()