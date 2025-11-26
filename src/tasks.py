from contextlib import asynccontextmanager
from typing import AsyncGenerator, List, Dict, Any

from src.database import AsyncSessionLocal, init_db
from src.services.data_parser import WikipediaParser
from src.services.db_operations import DBOperations


@asynccontextmanager
async def get_db_session() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        yield session


async def get_data_task() -> int:
    await init_db()

    parser = WikipediaParser()
    data = await parser.get_raw_data()
    if not data:
        return 0

    async with get_db_session() as session:
        db_op = DBOperations(session)
        await db_op.save_population_data(data)

    return len(data)


async def print_data_task() -> List[Dict[str, Any]]:
    async with get_db_session() as session:
        db_op = DBOperations(session)
        aggregated = await db_op.get_aggregated_region_data()

    return aggregated
