from services.budget_service import BudgetService

service = BudgetService()

print(service.get_months())

print(service.budget_summary("2026-07"))

print(service.budget_vs_actual("2026-07"))

service.close()
