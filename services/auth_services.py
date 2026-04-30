import asyncpg

from repositories import auth_repo as repo
from schemas.auth_schema import Auth
from errors import auth_errors as error
from core.security import create_access_token,create_refresh_token,hash_password,hash_token,verify_password


async def sign_up(conn: asyncpg.Connection,user: Auth) -> dict:
    user_exist = repo.username_exist(conn,user.username)
    if user_exist:
        raise error.UserALreadyExistError()
    hashed_password = hash_password(user.password)
    user_id = repo.create_user(conn,user.username,hashed_password)
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)
    hashed_refresh_token = hash_token(refresh_token)
    repo.add_refresh_token(conn,user_id,hashed_refresh_token)
    return {
        "access_token" : access_token,
        "refresh_token" : refresh_token
    }
async def log_in(conn: asyncpg.Connection,user: Auth):
    user_exist = repo.username_exist(conn,user.username)
    if not user_exist:
        raise error.UserNotExistError()
    hash_password = repo.fetch_password(conn,user.username)
    password_correct = verify_password(user.password,hash_password)
    if not password_correct:
        raise error.WrongPasswordError()
    user_id = repo.fetch_user_id(conn,user.username)
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)
    hashed_refresh_token = hash_token(refresh_token)
    repo.replace_refresh_token(conn,user_id,hashed_refresh_token)
    repo.make_user_active(conn,)
    


