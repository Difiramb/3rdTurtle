from fastapi import FastAPI

app = FastAPI(title="MLBB Esports API", version="0.1.0")


@app.get("/api/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Return a lightweight readiness response without querying the database."""
    return {"status": "ok"}
