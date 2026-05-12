from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status , Response
from .user import UserService
from ..schema.user import UserLogin,MessageCreate
from ..core.security import verify_password,loginTokens
from sqlalchemy import select
from ..core.config import settings
from ..model.model import User
from email.mime.text import MIMEText
import smtplib

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db
        self.user_service = UserService(db)

    async def login_user(self, user_input: UserLogin, response: Response):
        stmt = select(User).where(User.email == user_input.email)
        result = await self.db.execute(stmt)
        user = result.scalars().first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not verify_password(user_input.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        token_data = loginTokens(user.id)

        access_token = token_data["access_token"]
        refresh_token = token_data["refresh_token"]

        # Set cookie max_age in seconds. Use REFRESH_TOKEN_EXPIRE_MINUTES from settings.
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="None",
            max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
            path="/",
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "id": user.id,
            "username": user.user_name,
            "email": user.email,
            "phone_no": user.phone_no,
            "role" : user.role,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }
        
    async def get_service_by_email(self, Service_email :str):
        result = await self.db.execute(select(User).where(User.email == Service_email))
        return result.scalars().first()
       
    async def get_profile(self, Service_email:str):
        result = await self.get_service_by_email(Service_email)
        return {
            "email" : result.email,
            "username" : result.user_name,
            "phone_no" : result.phone_no
        }
        
def send_email_background(user_input: MessageCreate):
    body = f"""
    New Message Received

    Name: {user_input.name}
    Email: {user_input.email}
    Phone: {user_input.phone_no}

    Message:
    {user_input.message}
    """
    msg = MIMEText(body)
    msg["Subject"] = user_input.subject
    msg["From"] = user_input.email
    msg["To"] = settings.EMAIL_ADDRESS

    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
        server.send_message(msg)
