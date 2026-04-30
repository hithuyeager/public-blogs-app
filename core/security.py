from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError,VerificationError,InvalidHashError
from jose import JWTError,jwt,ExpiredSignatureError
from datetime import datetime,timedelta,timezone
import hashlib



from core.config import settings
from errors.auth_errors import ExpiredTokenError,InvalidTokenError,InvalidTokenTypeError


#----------------------password management------------------------------------------
ph = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=32,
    salt_len=16
)

def hash_password(plain_password: str) -> str:
    return ph.hash(plain_password)
def verify_password(plain_password:str , hash_password: str) -> bool:
    try:
        ph.verify(hash_password,plain_password)
        return True
    except (VerifyMismatchError,VerificationError,InvalidHashError):
        return False

#--------------------------JWT Management----------------------------------------------

def create_access_token(user_id: str) -> str:
    payload = {
        "sub" : user_id,
        "exp" : datetime.now(timezone.utc) + timedelta(minutes = settings.access_token_expire),
        "type" : "access"
    }
    return jwt.encode(payload,settings.secret_key, algorithm = settings.algorithm,)

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token,settings.secret_key,algorithms=[settings.algorithm])
        if payload.get("type") != "access":
            raise InvalidTokenTypeError()
        return payload
    except ExpiredSignatureError:
        raise ExpiredTokenError()
    except JWTError:
        raise InvalidTokenError()
    
def create_refresh_token(user_id:str) -> str:
    payload = {
        "sub" : user_id,
        "exp" : datetime.now(timezone.utc) + timedelta(days = settings.refresh_token_expire),
        "type" : "refresh"
    }
    return jwt.encode(payload,settings.secret_key, algorithm = settings.algorithm,)

def token_rotation(old_refresh_token: str) -> dict:
    try:
        payload = jwt.decode(old_refresh_token,settings.secret_key,algorithms=[settings.algorithm])
    except ExpiredSignatureError:
        raise ExpiredTokenError()
    except JWTError:
        raise InvalidTokenError()
    else:
        user_id = payload.get("sub")
        access_token = create_access_token(user_id)
        refresh_token = create_refresh_token(user_id)
        return {
            "access_token" : access_token,
            "refresh_token" : refresh_token
        }
    
#----------------------------token hashings-------------------------------------------------------

def hash_token(refresh_token: str) -> str:
    return hashlib.sha256(refresh_token.encode()).hexdigest()
def compare_hash_token(plain: str,hashed_token: str) -> bool:
    return hash_token(plain) == hashed_token
    

