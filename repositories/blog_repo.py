import asyncpg
from uuid import UUID

async def create_blog(conn: asyncpg.Connection,user_id: UUID,title: str ,blog: str) -> bool:
    status = await conn.fetchval("INSERT INTO users_blogs (user_id,title,blog) VALUES ($1,$2,$3) RETURNING true",UUID(user_id),title,blog)
    return status

async def update_blog(conn: asyncpg.Connection,user_id: UUID ,id: int,blog: str) -> bool:
    status = await conn.fetchval("UPDATE users_blogs SET blog = $3 ,updated_at = NOW() WHERE id = $2 AND user_id = $1 RETURNING true",user_id,id,blog)
    return status

async def fetch_all_user_blogs(conn: asyncpg.Connection,user_id: UUID,offset: int,limit: int) -> dict:
    rows = await conn.fetch("SELECT id,blog,title,created_at,updated_at FROM users_blogs WHERE user_id = $1 OFFSET $2 LIMIT $3",user_id,offset,limit)
    return [dict(row) for row in rows]
async def fetch_blogs_count(conn: asyncpg.Connection,user_id: UUID) -> int:
    count = await conn.fetchval("SELECT COUNT(blog) FROM users_blogs WHERE user_id = $1",user_id)
    return count

async def fetch_one_blog(conn: asyncpg.Connection,user_id: UUID , blog_id: int) -> dict:
    single_blog = await conn.fetchrow("SELECT blog from users_blogs WHERE id = $2 AND user_id = $1",user_id,blog_id)
    return dict(single_blog)
