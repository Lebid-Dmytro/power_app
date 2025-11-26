import os


class Config:
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://user:password@db:5432/population_db"
    )
