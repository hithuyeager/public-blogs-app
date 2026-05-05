import asyncpg
from uuid import UUID

from repositories import blog_repo as repo
from errors import blog_errors as error

async def create_blog(conn: asyncpg.Connection ,user_id: UUID ,title: str ,blog: str) -> bool:
    status = await repo.create_blog(conn,user_id,title,blog)
    if not status:
        raise error.CreatingBlogError()
    return True
async def get_user_blogs(conn: asyncpg.Connection,user_id: UUID,offset: int,limit: int) -> dict:
    blogs_count = await repo.fetch_blogs_count(conn,user_id)
    if blogs_count < offset:
        raise error.BlogsOutOfRangeError()
    if offset < 1 or limit < 1:
        raise error.NegativeOffsetLimitError()
    data = await repo.fetch_all_user_blogs(conn,user_id,offset,limit)
    return data
