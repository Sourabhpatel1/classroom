from fastapi import APIRouter
from users.routes import user_router
from jwt_token.routes import token_router


base_router = APIRouter()

base_router.include_router(user_router, prefix="/users", tags=['users'])
base_router.include_router(token_router, prefix="/token", tags=["token"])
