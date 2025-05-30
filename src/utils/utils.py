from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
import uuid
from src.utils.config import settings
import logging


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)
    
    
def create_access_token(user_data:dict, expiry:timedelta, refresh:bool=False):
    payload = {
        "user":user_data,
        "exp": datetime.utcnow() + (expiry if not expiry else timedelta(minutes=60)),
        "jti": str(uuid.uuid4()),
        "refresh": refresh
    }
    
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    return token

def decode_access_token(token: str): 
    try:
        token_data = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return token_data
    except jwt.PyJWTError as e:
        logging.error(f"Token decoding failed: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None