from pathlib import Path
import pdfplumber

from utils.file_utils import calculate_file_hash

from services.database import (
    add_processed_file,
    file_already_processed
)


class BasePDFParser:

    def __init__(self, pdf_file, source):

        self.pdf_file = Path(pdf_file)
        self.source = source

        self.inserted = 0
        self.duplicates = 0

    def extract_text(self):

        print("=" * 70)
        print(self.source.upper())
        print("=" * 70)

        text = ""

        with pdfplumber.open(self.pdf_file) as pdf:

            print(f"Pages : {len(pdf.pages)}")

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        print(f"Characters Extracted : {len(text)}")

        return text

    def is_file_processed(self):

        file_hash = calculate_file_hash(self.pdf_file)

        print("Current Hash :", file_hash)

        result = file_already_processed(file_hash)

        print("file_already_processed() returned ->", result)

        if result:
            print("File already imported.")
            return True

        self.file_hash = file_hash

        print("Returning False")

        return False

    def mark_completed(self):

        add_processed_file(
            self.pdf_file.name,
            self.file_hash,
            self.source
        )

    def print_summary(self, total):

        print()

        print("=" * 70)

        print("IMPORT SUMMARY")

        print("=" * 70)

        print(f"Transactions Found : {total}")
        print(f"Inserted           : {self.inserted}")
        print(f"Duplicates         : {self.duplicates}")

        print("=" * 70)