from ...core.dependencies import SessionDep
from typing import Annotated
from fastapi import Depends
from .schemas import TokenData
from fastapi.security import OAuth2PasswordBearer
import jwt
from pwdlib import PasswordHash # type: ignore
from os import getenv
from dotenv import load_dotenv
from ...api.user.service import UserService
from ...core.exceptions import CredentialsException
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from uuid import UUID
from ..user.schemas import UserResponse

load_dotenv()

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hasher = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hasher.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return password_hasher.hash(password)

def authenticate_user(user_service: UserService, email: str, password: str) -> UserResponse | None:
    user = user_service.get_by_email(email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(email: str, user_id: UUID, expires_delta: timedelta = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {
        "sub": email,
        "id": str(user_id),
        "exp": expire
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def _decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        user_id = payload.get("id")
        if email is None or user_id is None:
            raise CredentialsException()
        return TokenData(email=email, user_id=user_id)
    except InvalidTokenError:
        raise CredentialsException()

def _get_user(db: SessionDep, email: str):
    user_service = UserService(db)
    return user_service.get_by_email(email)

async def get_current_user(db: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    token_data = _decode_token(token)
    user = _get_user(db, token_data.email)
    if user is None:
        raise CredentialsException()
    return token_data