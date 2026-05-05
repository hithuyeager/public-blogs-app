import asyncpg
from uuid import UUID

async def create_blog(conn: asyncpg.Connection,user_id: UUID,title: str ,blog: str) -> bool:
    status = await conn.fetchval("INSERT INTO users_blogs (user_id,title,blog) VALUES ($1,$2,$3) RETURNING true",UUID(user_id),title,blog)
    return status

async def update_blog(conn: asyncpg.Connection,id: UUID,blog: str) -> bool:
    status = await conn.fetchval("UPDATE users_blogs SET blog = $2 ,updated_at = NOW() WHERE id = $1 RETURNING true",id,blog)
    return status

async def fetch_all_user_blogs(conn: asyncpg.Connection,user_id: UUID,offset: int,limit: int) -> dict:
    rows = await conn.fetch("SELECT id,blog,title,created_at,updated_at FROM users_blogs WHERE user_id = $1 OFFSET $2 LIMIT $3",user_id,offset,limit)
    return [dict(row) for row in rows]

