import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


def build_database_url() -> str:
    """Build the PostgreSQL URL from environment variables."""
    return (
        "postgresql+psycopg2://"
        f"{os.getenv('POSTGRES_USER', 'mlbb_admin')}:"
        f"{os.getenv('POSTGRES_PASSWORD', 'supersecretpassword')}@"
        f"{os.getenv('POSTGRES_HOST', 'localhost')}:"
        f"{os.getenv('POSTGRES_PORT', '5433')}/"
        f"{os.getenv('POSTGRES_DB', 'mlbb_esports')}"
    )


DATABASE_URL = os.getenv("DATABASE_URL", build_database_url())


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    """Provide a database session for FastAPI dependencies."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
