from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse

from schemas.auth_schema import Auth
from core.dependencies import get_connection
from services.auth_services import sign_up,log_in,rotate_token
from core.responses import APIResponse

router = APIRouter(prefix="/auth")

@router.post("/signup")
async def signup(user: Auth ,conn = Depends(get_connection)):
    result = await sign_up(conn,user.username,user.password)
    result.update({"token-type" : "bearer"})
    return JSONResponse(
        status_code=202,
        content=APIResponse(
            status="success",
            data = result
        ).model_dump()
    )
@router.post("/login")
async def login(user: Auth,conn = Depends(get_connection)):
    result = await log_in(conn,user.username,user.password)
    result.update({"token-type" : "bearer"})
    return JSONResponse(
        status_code=200,
        content=APIResponse(
            status="success",
            data = result
        ).model_dump()
    )

@router.patch("/tokenrotation")
async def tokenrotation(refresh_token: str,conn = Depends(get_connection)):
    result = await rotate_token(conn,refresh_token)
    result.update({"token-type" : "bearer"})
    return JSONResponse(
        status_code=200,
        content=APIResponse(
            status="success",
            data = result
        ).model_dump()
    )

