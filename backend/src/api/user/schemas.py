from pydantic import BaseModel

class UserRegister(BaseModel):
    email: str
    password: str
    
class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    full_name: str | None = None
    
class UserPatch(BaseModel):
    pfp_url: str | None = None
    bio: str | None = None
    location: str | None = None