from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.db import get_session
from src.v1.schemas.auth import UserCreate, UserOut
from src.v1.service.auth import AuthService
from src.v1.models.models import User

auth_router = APIRouter()
auth_service = AuthService()



@auth_router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(new_user:UserCreate, session:AsyncSession = Depends(get_session)):
    """
    Register a new user.
    """
    user = await auth_service.create_user(user_dict=new_user, session=session)
    return user

@auth_router.get("/user/{email}", response_model=UserOut)
async def get_user_by_email(email: str, session: AsyncSession = Depends(get_session)):
    """
    Get user by email.
    """
    user = await auth_service.get_user_by_email(email=email, session=session)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user

@auth_router.put("/user/update", response_model=UserOut)
async def update_user(user_update: UserCreate, session: AsyncSession = Depends(get_session)):
    """
    Update user details.
    """
    user = await auth_service.update_user(user_dict=user_update, session=session)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user