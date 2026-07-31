from services.analytics_service import AnalyticsService

analytics = AnalyticsService()

print("=" * 60)

print("Total Spending")
print(analytics.total_spending())

print()

print("Total Income")
print(analytics.total_income())

print()

print("Top Merchants")
print(analytics.top_merchants())

print()

print("Category Spending")
print(analytics.spending_by_category())

print()

print("Monthly Spending")
print(analytics.monthly_spending_df())

print()
print("=" * 60)
print("TOP UNCATEGORIZED MERCHANTS")
print("=" * 60)

print(analytics.uncategorized_merchants())

analytics.close()