from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import asyncpg
from uuid import UUID

from services.blog_services import (create_blog,get_user_blogs)
from core.dependencies import (get_connection,get_current_user)
from schemas.blog_schema import Title,Blogs
from core.responses import APIResponse

router = APIRouter()

@router.post("/create")
async def create_blogs(
    title: Title,
    blog: Blogs,
    conn: asyncpg.Connection = Depends(get_connection),
    user_id: UUID = Depends(get_current_user),
    ) -> dict:
    await create_blog(conn,user_id,title.title,blog.blogs)
    return JSONResponse(
        status_code=202,
        content=APIResponse(
            status = "success",
            data = "created succesfully"
        ).model_dump()
    )
@router.get("/fetch")
async def fetch_users_blogs(offset: int ,limit: int,conn: asyncpg.Connection = Depends(get_connection),user_id: UUID = Depends(get_current_user)) -> dict:
    paginated_blogs = await get_user_blogs(conn,user_id,offset,limit)
    return JSONResponse(
        status_code=200,
        content=APIResponse(
            status="success",
            data = jsonable_encoder(paginated_blogs)
        ).model_dump()
    )
