from src.utils.utils import create_access_token, decode_access_token
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi import Request,status
from fastapi.security.http import HTTPAuthorizationCredentials


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error= True):
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request:Request) -> HTTPAuthorizationCredentials:
        credentials = await super().__call__(request)
        token = credentials.credentials
        
        
        
        if not self.token_data(token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
        
        self.verify_token_data(token)
        
        return token
    
    def token_data(self, token: str) -> bool:
        token_data = decode_access_token(token)
        return token_data is not None
    
    def verify_token_data(self,token_data):
        NotImplementedError("Child classes handles")

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data:dict) -> None:
        if token_data and token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide an access Token")
        
class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data) -> None:
        if token_data and not token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide an refresh Token")

        
