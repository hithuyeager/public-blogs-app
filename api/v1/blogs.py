from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
import asyncpg
from uuid import UUID

from services.blog_services import (create_blog)
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
    status = await create_blog(conn,user_id,title.title,blog.blogs)
    return JSONResponse(
        status_code=200,
        content=APIResponse(
            status = "success",
            data = "created succesfully"
        ).model_dump()
    )