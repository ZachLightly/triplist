from ...core.dependencies import db_session
from .schemas import UserRegister, UserResponse
from .repo import UserRepo

class UserService:
    def __init__(self, db):
        self.repository = UserRepo(db)
        
    async def get_by_id(self, user_id: str) -> UserResponse | None:
        user = await self.repository.get_by_id(user_id)
        if user is None:
            return None
        return UserResponse(
            id=str(user.id),
            email=user.email,
            username=user.username,
            full_name=user.full_name | None
        )
        
    async def get_by_email(self, email: str) -> UserResponse | None:
        user = await self.repository.get_by_email(email)
        if user is None:
            return None
        return UserResponse(
            id=str(user.id),
            email=user.email,
            username=user.username,
            full_name=user.full_name | None
        )
        
    async def register_user(self, data: UserRegister) -> UserResponse:
        user = await self.repository.create_user(data)
        return UserResponse(
            id=str(user.id),
            email=user.email,
            username=user.username,
            full_name=user.full_name | None
        )