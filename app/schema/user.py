from pydantic import BaseModel,EmailStr,Field,field_validator
from typing import Optional
from ..schema.enum import UserRole

class MessageCreate(BaseModel):
    name: str = Field(max_length=20,min_length=3)
    email: EmailStr 
    phone_no: str = Field(max_length=18,min_length=8)
    subject: str
    message: Optional[str] = Field(max_length=300)


# ------------------------------------if we pass " " default role = user------------------------------------

class UserCreate(BaseModel):
    user_name: str= Field(min_length=4)
    email: EmailStr 
    phone_no: str = Field(max_length=18,min_length=8)
    role: UserRole = UserRole.user
    @field_validator("role", mode="before")
    @classmethod
    def empty_string_to_default(cls, v):
        if v == "":
            return UserRole.user
        return v
    password: str = Field(min_length=8,max_length=16)
   
   
class UserLogin(BaseModel):
    email: str = Field(...,description="email")
    password : str = Field(...,min_length=6,max_length=18)
    
# class LogoutUser(BaseModel):
#     email: str | None
#     id: str | None