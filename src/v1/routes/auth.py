from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.dependencies import AccessTokenBearer, get_current_user
from src.db.db import get_session
from src.utils.config import settings
from src.utils.utils import create_access_token, verify_password
from src.v1.schemas.auth import UserCreate, UserOut
from src.v1.service.auth import AuthService

auth_router = APIRouter()
auth_service = AuthService()


@auth_router.post(
    "/register", response_model=UserOut, status_code=status.HTTP_201_CREATED
)
async def register_user(
    new_user: UserCreate, session: AsyncSession = Depends(get_session)
):
    """
    Register a new user.
    """

    user_email = new_user.email

    user_exists = await auth_service.user_exist(email=user_email, session=session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    user = await auth_service.create_user(user_dict=new_user, session=session)

    return user


@auth_router.post("/login")
async def login_user(
    user_login: UserCreate, session: AsyncSession = Depends(get_session)
):
    user_email = user_login.email
    user_password = user_login.password

    user = await auth_service.get_user_by_email(email=user_email, session=session)

    if user is not None:
        password_valid = verify_password(user_password, user.hashed_password)
        if password_valid:
            access_token = create_access_token(
                user_data={"email": user.email, "uid": str(user.uid)},
                expiry=timedelta(minutes=settings.access_token_expiry),
            )
            refresh_token = create_access_token(
                user_data={"email": user.email, "uid": str(user.uid)},
                expiry=timedelta(minutes=settings.refresh_token_expiry),
                refresh=True,
            )

        return JSONResponse(
            content={
                "message": "Login successful",
                "tokens": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
                "user": {"email": user.email, "uid": str(user.uid)},
            },
            status_code=status.HTTP_200_OK,
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
    )


@auth_router.get("/me", status_code=status.HTTP_200_OK)
async def get_current_user(user=Depends(get_current_user)):
    return user


@auth_router.get("/user/{email}", response_model=UserOut)
async def get_user_by_email(email: str, session: AsyncSession = Depends(get_session)):
    """
    Get user by email.
    """
    user = await auth_service.get_user_by_email(email=email, session=session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user