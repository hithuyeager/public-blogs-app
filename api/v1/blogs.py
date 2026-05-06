from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import asyncpg
from uuid import UUID

from services.blog_services import (create_blog,get_user_blogs,blog_update,get_single_blog,remove_user_blog)
from core.dependencies import (get_connection,get_current_user)
from schemas.blog_schema import Title,Blogs,UpdateBlog
from core.responses import APIResponse

router = APIRouter()

@router.post("/create")
async def create_blogs(
    title: Title,
    blog: Blogs,
    conn: asyncpg.Connection = Depends(get_connection),
    user_id: UUID = Depends(get_current_user),
) -> JSONResponse:
    await create_blog(conn,user_id,title.title,blog.blogs)
    return JSONResponse(
        status_code=202,
        content=APIResponse(
            status = "success",
            data = "created succesfully"
        ).model_dump()
    )
@router.get("/fetch")
async def fetch_users_blogs(
    offset: int ,
    limit: int,
    conn: asyncpg.Connection = Depends(get_connection),
    user_id: UUID = Depends(get_current_user)
) -> JSONResponse:
    paginated_blogs = await get_user_blogs(conn,user_id,offset,limit)
    return JSONResponse(
        status_code=200,
        content=APIResponse(
            status="success",
            data = jsonable_encoder(paginated_blogs)
        ).model_dump()
    )
@router.patch("/update")
async def update_blog(
    user: UpdateBlog,
    conn: asyncpg.Connection = Depends(get_connection),
    user_id: UUID = Depends(get_current_user)
) -> JSONResponse:
    await blog_update(conn,user_id,user.blog_id,user.blog)
    return JSONResponse(
        status_code = 202,
        content = APIResponse(
            status = "success",
            data = "updated successfully"
        ).model_dump()
    )

@router.get("/singleblog")
async def fetch_single_blog(
    blog_id: int,
    user_id: UUID = Depends(get_current_user),
    conn: asyncpg.Connection = Depends(get_connection)
) -> JSONResponse:
    single_blog = await get_single_blog(conn,user_id,blog_id)
    return JSONResponse(
        status_code = 200,
        content = APIResponse(
            status = "success",
            data = single_blog
        ).model_dump()
    )
@router.delete("/removeblog")
async def delete_user_blog(
    blog_id: int,
    user_id: UUID = Depends(get_current_user),
    conn: asyncpg.Connection = Depends(get_connection)
) -> JSONResponse:
    await remove_user_blog(conn,user_id,blog_id)
    return JSONResponse(
        status_code = 200,
        content = APIResponse(
            status = "success",
            data = "deleted successfully"
        ).model_dump()
    )
    