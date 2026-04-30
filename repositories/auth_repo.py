import asyncpg
from uuid import UUID

async def create_user(conn: asyncpg.Connection,username: str,password: str) -> str:
    user_id = conn.fetchval(" INSERT INTO users_auth (username,password) VALUES ($1,$2) RETURNING id",username,password)
    return str(user_id)
async def username_exist(conn: asyncpg.Connection,username: str) -> bool:
    user = conn.fetchrow("SELECT * FROM users_auth WHERE username = $1",username)
    if user is None:
        return False
    return True

async def fetch_user_id(conn:asyncpg.Connection,username: str) -> str:
    user_id = conn.fetchval("SELECT id FROM users_auth WHERE username = $1",username)
    return user_id
async def fetch_password(conn: asyncpg.Connection ,username: str) -> str:
    hash_password = conn.fetchval("SELECT password FROM users_auth WHERE username = $1",username)



async def add_refresh_token(conn: asyncpg.Connection,user_id: UUID,refresh_token: str) -> str:
    status = conn.fetchval("INSERT INTO users_session (user_id,hash_refresh_token) VALUES ($1,$2) RETURNING id",user_id,refresh_token)
    return str(status)
async def fetch_refresh_token(conn: asyncpg.Connection,user_id: str) -> str:
    hashed_refresh_token = conn.fetchval("SELECT hash_refresh_token FROM user_session WHERE user_id = $1",user_id)
    return hashed_refresh_token

