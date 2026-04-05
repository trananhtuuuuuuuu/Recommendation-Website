# Run project on locally environment
```bash
# run inside DATN path
uvicorn main:app --reload
```

# Run migration for each time anyone who would like to change database structure with the purpose creating migration files inside /migrations/version/"filename" run inside DATN/app path
```bash
uv run alembic revision --autogenerate -m "describe your change here"
```

# Apply all of migration files to create new database structure
```bash
uv run alembic upgrade head
```