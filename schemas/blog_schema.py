from pydantic import BaseModel,Field

class Title(BaseModel):
    title: str = Field(min_length=1,max_length=50)

class Blogs(BaseModel):
    blogs: str = Field(min_length=1)

class Pagination(BaseModel):
    offset: int = Field(gt=0)
    limit: int = Field(gt=0,lt=50)
    