from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager


from database.db_connections import create_pool
from errors.auth_errors import AuthError
from core.responses import APIResponse
from api.central_apis import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await create_pool()
    yield
    await app.state.pool.close()

app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.exception_handler(AuthError)
async def global_exception_handler(request: Request , exc: AuthError):
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(
            status = "error",
            data = exc.message
        ).model_dump()
    )
