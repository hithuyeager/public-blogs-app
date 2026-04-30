from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.db_connections import create_pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await create_pool()
    yield
    await app.state.pool.close()

app = FastAPI(lifespan=lifespan)
