import asyncpg
from core.config import settings

async def create_pool():
    return await asyncpg.create_pool(
        dsn = settings.database_url,
        min_size = 5,
        max_size = 20,
        command_timeout = 60
    )

