import asyncpg
from uuid import UUID


#--------------------------------------users auth table----------------------------------------------------------

async def create_user(conn: asyncpg.Connection,username: str,password: str) -> str:
    user_id = await conn.fetchval(" INSERT INTO users_auth (username,password) VALUES ($1,$2) RETURNING id",username,password)
    return str(user_id)
async def username_exist(conn: asyncpg.Connection,username: str) -> bool:
    user = await conn.fetchrow("SELECT * FROM users_auth WHERE username = $1",username)
    if user is None:
        return False
    return True

async def fetch_user_id(conn:asyncpg.Connection,username: str) -> str:
    user_id = await conn.fetchval("SELECT id FROM users_auth WHERE username = $1",username)
    return str(user_id)
async def fetch_password(conn: asyncpg.Connection ,username: str) -> str:
    hash_password = await conn.fetchval("SELECT password FROM users_auth WHERE username = $1",username)
    return hash_password


#--------------------------------------user session table---------------------------------------------------------

async def add_refresh_token(conn: asyncpg.Connection,user_id: UUID,refresh_token: str) -> str:
    status = await conn.fetchval("INSERT INTO user_session (user_id,hash_refresh_token) VALUES ($1,$2) RETURNING id",user_id,refresh_token)
    return str(status)
async def fetch_refresh_token(conn: asyncpg.Connection,user_id: UUID) -> str:
    hashed_refresh_token = await conn.fetchval("SELECT hash_refresh_token FROM user_session WHERE user_id = $1",user_id)
    return hashed_refresh_token
async def replace_refresh_token(conn: asyncpg.Connection,user_id: UUID,hashed_refresh_token: str) -> str:
    status = await conn.fetchval("UPDATE user_session SET hash_refresh_token = $2 WHERE user_id = $1 RETURNING id",user_id,hashed_refresh_token)
    return str(status)
async def make_user_active(conn: asyncpg.Connection,user_id: UUID) -> str:
    status = await conn.fetchval("UPDATE user_session SET is_active = true WHERE user_id = $1 RETURNING id",user_id)
    return str(status)
async def fetch_user_status(conn: asyncpg.Connection,user_id: UUID) -> bool:
    is_active = await conn.fetchval("SELECT is_active FROM user_session WHERE user_id = $1",user_id)
    return is_active
