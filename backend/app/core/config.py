from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Operations & Supply Chain Analytics API"
    database_url: str = "postgresql+psycopg://analytics:analytics_password@db:5432/operations_analytics"
    cors_origins: list[str] = ["http://localhost:5175", "http://127.0.0.1:5175"]


settings = Settings()
