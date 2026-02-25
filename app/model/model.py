from ..database.database import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import Integer,String,DateTime,func
from datetime import datetime
from ..schema.user import UserRole
from enum import Enum

class User(Base):
    __tablename__ = "users"
    
    id: Mapped [int] = mapped_column(Integer, primary_key = True)
    user_name: Mapped [str] = mapped_column(String, nullable= False)
    email: Mapped [str] = mapped_column(String, nullable= False, unique=True)
    phone_no: Mapped [str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, names="userrole"),default=UserRole.user,nullable=False)
    password: Mapped [str] = mapped_column(String , nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())