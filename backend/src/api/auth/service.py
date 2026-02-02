from ...core.dependencies import db_session
from ..user.service import UserService
from . import auth
from ..user.schemas import UserRegister, UserResponse
from .schemas import Token
from ...core.exceptions import CredentialsException, UserAlreadyExistsException
from uuid import UUID


class AuthService:
    def __init__(self, db: db_session):
        self.user_service = UserService(db)

    async def login_for_access_token(self, email: str, password: str) -> Token:
        user = await auth.authenticate_user(self.user_service, email, password)
        if not user:
            raise CredentialsException()
        access_token = auth.create_access_token(user.email, UUID(user.id))
        return Token(access_token=access_token)

    async def register_user(self, data: UserRegister) -> UserResponse:
        existing_user = await self.user_service.get_by_email(data.email)
        if existing_user:
            raise UserAlreadyExistsException(email=data.email)
        data.password = auth.get_password_hash(data.password)
        user = await self.user_service.register_user(data)
        return UserResponse.model_validate(user)