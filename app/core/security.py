from passlib.context import CryptContext
from .config import settings
from jose import jwt
from datetime import datetime,timedelta,timezone
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

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt