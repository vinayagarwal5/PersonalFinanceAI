import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from analytics.analytics_service import AnalyticsService

analytics = AnalyticsService()

print("=" * 60)
print("PERSONAL FINANCE REPORT")
print("=" * 60)

print()

print("Total Spending")
print(analytics.total_spending())

print()

print("Total Income")
print(analytics.total_income())

print()

print("Monthly Spending")

for row in analytics.monthly_spending():
    print(row)

print()

print("Top Merchants")

for row in analytics.top_merchants():
    print(row)

analytics.close()