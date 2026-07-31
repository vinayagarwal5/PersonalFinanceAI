from datetime import datetime


def convert_date(date_str, input_format):
    """
    Generic date conversion.

    Example:
        convert_date("Jul 21, 2025", "%b %d, %Y")
        -> 2025-07-21

        convert_date("14-NOV-24", "%d-%b-%y")
        -> 2024-11-14
    """

    return datetime.strptime(
        date_str,
        input_format
    ).strftime("%Y-%m-%d")


def get_month(date_str, input_format):
    """
    Returns YYYY-MM
    """

    dt = datetime.strptime(date_str, input_format)

    return dt.strftime("%Y-%m")


def get_financial_year(date_str, input_format):
    """
    Returns FY in format 2025-26
    """

    dt = datetime.strptime(date_str, input_format)

    if dt.month >= 4:
        start = dt.year
    else:
        start = dt.year - 1

    return f"{start}-{str(start+1)[-2:]}"