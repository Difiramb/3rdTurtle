# MLBB Esports Project

## Run the API

```bat
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/api/health`. The expected response is:

```json
{"status":"ok"}
```

## Database configuration

By default, the application connects to the local PostgreSQL instance supplied for this project:

`postgresql+psycopg2://mlbb_admin:supersecretpassword@localhost:5433/mlbb_esports`

For other environments, set `DATABASE_URL` (preferred), or set the individual `POSTGRES_USER`,
`POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`, and `POSTGRES_DB` environment variables.

## Create and apply the initial migration

With the virtual environment active and PostgreSQL running:

```bat
alembic revision --autogenerate -m "create initial schema"
alembic upgrade head
```

Inspect the current migration state with:

```bat
alembic current
```
