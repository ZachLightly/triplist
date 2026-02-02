from typing import Annotated
from fastapi import Depends
from ..api.auth.schemas import TokenData
from ..api.auth.auth import get_current_user

from .db import Session, get_db

db_session = Annotated[Session, Depends(get_db)]

current_user = Annotated[TokenData, Depends(get_current_user)]

