import asyncpg

from repositories import auth_repo as repo
from schemas.auth_schema import Auth
from errors import auth_errors as error
from core.security import create_access_token,create_refresh_token,hash_password,hash_token,verify_password,token_rotation,decode_refresh_token


async def sign_up(conn: asyncpg.Connection,user: Auth) -> dict:
    user_exist = await repo.username_exist(conn,user.username)
    if user_exist:
        raise error.UserALreadyExistError()
    hashed_password = hash_password(user.password)
    user_id = await repo.create_user(conn,user.username,hashed_password)
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)
    hashed_refresh_token = hash_token(refresh_token)
    await repo.add_refresh_token(conn,user_id,hashed_refresh_token)
    return {
        "access_token" : access_token,
        "refresh_token" : refresh_token
    }
async def log_in(conn: asyncpg.Connection,user: Auth):
    user_exist = await repo.username_exist(conn,user.username)
    if not user_exist:
        raise error.UserNotExistError()
    hash_password = await repo.fetch_password(conn,user.username)
    password_correct = verify_password(user.password,hash_password)
    if not password_correct:
        raise error.WrongPasswordError()
    user_id = await repo.fetch_user_id(conn,user.username)
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)
    hashed_refresh_token = hash_token(refresh_token)
    await repo.replace_refresh_token(conn,user_id,hashed_refresh_token)
    await repo.make_user_active(conn,user_id)
    return {
        "access_token" : access_token,
        "refresh_token" : refresh_token
    }

async def rotate_token(conn:asyncpg.Connection,refresh_token):
    payload = decode_refresh_token(refresh_token)
    user_id = payload.get("sub")
    hashed_refresh_token = await repo.fetch_refresh_token(conn,user_id)
    active = await repo.fetch_user_status(conn,user_id)
    if (hashed_refresh_token != hash_token(refresh_token)) or (not active):
        raise error.TokenStolenError()
    data = token_rotation(refresh_token)
    new_refresh_token = data.get("refresh_token")
    new_hashed_refresh_token = hash_token(new_refresh_token)
    await repo.add_refresh_token(conn,user_id,new_hashed_refresh_token)
    return {
        "access_token" : data.get("access_token"),
        "refresh_token" : data.get("refresh_token")
    }