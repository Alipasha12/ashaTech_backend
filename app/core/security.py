from passlib.context import CryptContext
import hashlib 

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

MAX_BCRYPT_BYTES = 72


def prepare_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > MAX_BCRYPT_BYTES:
        return hashlib.sha256(password_bytes).hexdigest()
    return password


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str):
    return pwd_context(plain_password,hashed_password)