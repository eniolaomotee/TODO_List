from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.utils.utils import decode_access_token, hash_password
from src.v1.models.models import User
from src.v1.schemas.auth import UserCreate


class AuthService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        "Check if a user exists in the database by email."
        statement = select(User).where(User.email == email)

        result = await session.exec(statement)

        user = result.first()

        return user

    async def user_exist(self, email: str, session: AsyncSession):
        "Check if a user exists in the db"
        user = await self.get_user_by_email(email=email, session=session)

        return True if user else False

    async def create_user(self, user_dict: UserCreate, session: AsyncSession):
        "Create new user"
        user_email = user_dict.email
        user = await self.user_exist(email=user_email, session=session)

        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

        new_user_obj = user_dict.model_dump()

        new_user = User(**new_user_obj)

        new_user.hashed_password = hash_password(user_dict.password)

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    async def update_user(self, user_dict: UserCreate, session: AsyncSession):
        "Update user details"
        user_email = user_dict.email
        user = await self.get_user_by_email(email=user_email, session=session)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        for key, value in user_dict.model_dump().items():
            setattr(user, key, value)

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user
