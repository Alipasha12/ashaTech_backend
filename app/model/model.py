from ..database.database import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import Integer,String,DateTime,func,JSON
from datetime import datetime
from ..schema.user import UserRole
from enum import Enum
from sqlalchemy import Enum as SQLEnum

# User Table
class User(Base):
    __tablename__ = "users"
    
    id: Mapped [int] = mapped_column(Integer, primary_key = True)
    user_name: Mapped [str] = mapped_column(String, nullable= False)
    email: Mapped [str] = mapped_column(String, nullable= False, unique=True)
    phone_no: Mapped [str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(
    SQLEnum(UserRole, name="userrole"),
    default=UserRole.user,
    nullable=False
)
    password: Mapped [str] = mapped_column(String , nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
    
# blog table

class Blog(Base):
    __tablename__ = "blogs"
    
    id: Mapped [int] = mapped_column(Integer, primary_key=True)
    img: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String)
    introduction: Mapped[dict] = mapped_column(JSON)
    section: Mapped[list] = mapped_column(JSON)
    conclusion: Mapped[str] = mapped_column(String)
    contact_information : Mapped[str] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
    
# Service table

class Service(Base):
    __tablename__ = "services"
    
    id: Mapped [int] = mapped_column(Integer, primary_key=True)
    category: Mapped[str] = mapped_column(String)
    img: Mapped[str] = mapped_column(String)
    section: Mapped[dict] = mapped_column(JSON)
    choose_us: Mapped[dict] = mapped_column(JSON)
    section2: Mapped[list] = mapped_column(JSON)
    technologies: Mapped[list] = mapped_column(JSON)