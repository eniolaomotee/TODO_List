from src.utils.utils import create_access_token, decode_access_token
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi import Request,status, Depends
from fastapi.security.http import HTTPAuthorizationCredentials
from src.db.db import get_session
from src.v1.service.auth import AuthService
from abc import ABC, abstractmethod

auth_service = AuthService()
class TokenBearer(HTTPBearer, ABC):  
    def __init__(self, auto_error= True):
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials = await super().__call__(request)
        token = credentials.credentials
        token_data = decode_access_token(token)
        
        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        self.verify_token_data(token_data)
        
        
        return token_data

    @abstractmethod
    def verify_token_data(self, token_data: dict) -> None:
        pass        
    
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:

         if token_data.get("refresh", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an Access Token, not a Refresh Token",
            )
            
class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data.get("refresh",False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a Refresh Token, not an Access Token",
            )



async def get_current_user(token: dict = Depends(AccessTokenBearer()), session: AsyncSession = Depends(get_session)):
        """
        Dependency to get the current user from the access token.
        
        """
        user_email = token["user"]["email"]
                
        user = await auth_service.get_user_by_email(email=user_email, session=session)
        
        return user