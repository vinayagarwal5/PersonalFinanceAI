PersonalFinanceAI

Running migrations and helper scripts

- Recommended: run maintenance scripts as modules from the repository root to preserve package imports:

    python -m python.migrations.001_migrate_merchant_rules

- Convenience: scripts in python/ can also be executed directly; the project includes fallbacks so direct execution works, for example:

    python python\migrations\001_migrate_merchant_rules.py

- To inspect the database tables:

    python python\db\create_merchant_master.py  # creates merchant_master if missing

- To inspect the merchant_master schema and sample rows:

    python python\scripts\show_merchant_master.py

Notes:
- Prefer python -m when automating in CI to avoid sys.path hacks.
- The canonical merchant master schema uses `merchant_name` as the primary key.
- The current merchant_master schema also includes `is_active` and `last_updated`.
- If your database was created before migration 002, run:

    python python\migrations\002_alter_merchant_master.py

  to add these fields safely.
