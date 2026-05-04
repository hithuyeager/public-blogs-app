from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from fastapi import Depends,Request
from jose import ExpiredSignatureError,JWTError,jwt

from errors import auth_errors as error
from core.config import settings


bearer_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token,settings.secret_key,algorithms=[settings.algorithm])
        if payload["type"] != "access":
            raise error.InvalidTokenTypeError()
    except ExpiredSignatureError:
        raise error.ExpiredTokenError()
    except JWTError:
        raise error.InvalidTokenError()
    else:
        return payload.get("sub")
    
async def get_pool(request: Request):
    return request.app.state.pool

async def get_connection(pool = Depends(get_pool)):
    async with pool.acquire() as conn:
        yield conn

