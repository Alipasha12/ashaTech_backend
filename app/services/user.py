from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from ..schema.user import UserCreate
from ..model.model import User
from sqlalchemy import select
from ..core.security import get_password_hash


class UserService:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create_user(self, user_input: UserCreate):
        existing_user_by_email = await self.get_user_by_email(user_input.email)
        if existing_user_by_email:
            # raise ValueError(f"user with this {user_input.email} is already exist")
            raise  HTTPException(status_code=404, detail={"message": "user with this email already exist"})

        hashed_password = get_password_hash(user_input.password)
        user_input.password = hashed_password

        user_create = User(**user_input.model_dump())
        self.db.add(user_create)

        await self.db.commit()
        await self.db.refresh(user_create)
        return user_create

