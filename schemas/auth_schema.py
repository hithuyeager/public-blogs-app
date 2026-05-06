from pydantic import BaseModel,Field

class Auth(BaseModel):
    username: str = Field(min_length=8,max_length=12)
    password: str = Field(min_length=8)

class RefreshToken(BaseModel):
    refresh_token: str 