from ...core.dependencies import db_session
from ...core.models.user import User
from .schemas import UserRegister, UserPatch

class UserRepo:
    def __init__(self, db: db_session):
        self.db = db
        
    def get_by_id(self, user_id: str) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()    
    
    def create_user(self, data: UserRegister) -> User:
        user = User(
            username=data.email.split('@')[0],
            email=data.email,
            hashed_password=data.password
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user