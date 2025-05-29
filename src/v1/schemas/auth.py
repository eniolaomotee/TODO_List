from pydantic import BaseModel, EmailStr
import uuid
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password:str


class UserOut(BaseModel):
    uid: uuid.UUID
    is_active: bool 
    email: EmailStr
    created_at: datetime