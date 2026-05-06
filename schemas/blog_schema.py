from pydantic import BaseModel,Field

class CreateBlog(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    blogs: str = Field(min_length=1)
class UpdateBlog(BaseModel):
    blog_id: int
    blog: str

