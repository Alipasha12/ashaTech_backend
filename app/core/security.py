from passlib.context import CryptContext
from .config import settings
from jose import jwt
from datetime import datetime,timedelta
from pydantic import UUID4
import hashlib

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

MAX_BCRYPT_BYTES = 72

ALGORITHM = "HS256"

def prepare_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > MAX_BCRYPT_BYTES:
        return hashlib.sha256(password_bytes).hexdigest()
    return password


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict,expire_delta: timedelta | None = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt

def loginTokens(uuid: UUID4)-> dict:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(uuid)}, expire_delta = access_token_expires
    )
    refresh_token = create_access_token(
        data={"sub": str(uuid)}, expire_delta = refresh_token_expires
    )
    return{
        "access_token" : access_token,
        "refresh_token" : refresh_token,
        "token_type" : "bearer"
    }