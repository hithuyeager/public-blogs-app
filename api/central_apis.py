from fastapi import APIRouter
from .auth_router import router as auth_router
from .v1.blogs import router as blog_v1_router

router = APIRouter()
router.include_router(auth_router,prefix="/auth")
router.include_router(blog_v1_router,prefix="/blogs/v1")
