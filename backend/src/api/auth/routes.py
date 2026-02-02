from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from ..user.schemas import UserRegister, UserResponse
from ...core.dependencies import db_session, current_user
from .service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

# @router.post("/token", response_model=Token)
# async def login_for_access_token(db: DbSession, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
#     service = UserService(db)
#     return await service.login_for_access_token(form_data.username, form_data.password)

@router.post("/register", response_model=UserResponse)
async def register(db: db_session, data: UserRegister):
    service = AuthService(db)
    return await service.register_user(data)

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: current_user):
    return current_user