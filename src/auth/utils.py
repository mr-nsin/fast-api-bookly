from passlib.context import CryptContext
from datetime import timedelta, datetime
from src.config import Config
import jwt
import uuid
import logging

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRY = 3600

def gen_pass_hash(password: str) -> str:
    return pwd_cxt.hash(password)

def verify_pass(plain_password: str, hashed_password: str) -> bool:
    return pwd_cxt.verify(plain_password, hashed_password)    

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False) -> str:
    payload = {}
    payload['user'] = user_data.copy()
    expire = datetime.utcnow() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload.update({"exp": expire})
    payload.update({"jti": str(uuid.uuid4())})
    payload.update({"refresh": refresh})
    return jwt.encode(payload, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(token, Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
        return token_data
    except jwt.PyJWTError as e:
        logging.error(f"Error decoding token: {e}")
        return None
