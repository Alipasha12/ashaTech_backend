from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from .user import UserService
from ..schema.user import UserLogin
from ..core.security import verify_password,loginTokens
from sqlalchemy import select
from ..model.model import User


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db
        self.user_service = UserService(db)
        
    async def login_user(self, user_input: UserLogin):
        stmt = select(User).where(User.email == user_input.email)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

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
        
        return{
            "id": user.id,
            "username": user.user_name,
            "email": user.email,
            "phone_no": user.phone_no,
            "role" : user.role,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "login_token": token_data
        } 