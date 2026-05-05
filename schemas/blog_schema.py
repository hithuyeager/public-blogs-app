from pydantic import BaseModel,Field

class Title(BaseModel):
    title: str = Field(min_length=1,max_length=50)

class Blogs(BaseModel):
    blogs: str = Field(min_length=1)

class UpdateBlog(BaseModel):
    blog_id: int
    blog: str

