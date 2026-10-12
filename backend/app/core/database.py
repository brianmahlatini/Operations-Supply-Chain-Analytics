from sqlalchemy import create_engine, text
from sqlalchemy.engine import Result

from app.core.config import settings


engine = create_engine(settings.database_url, pool_pre_ping=True)


def fetch_all(query: str, params: dict | None = None) -> list[dict]:
    with engine.connect() as connection:
        result: Result = connection.execute(text(query), params or {})
        return [dict(row._mapping) for row in result]


def fetch_one(query: str, params: dict | None = None) -> dict:
    rows = fetch_all(query, params)
    return rows[0] if rows else {}
