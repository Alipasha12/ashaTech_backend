from pydantic import BaseModel,EmailStr
from typing import Optional,List

class introduction(BaseModel):
    overview: str
 
class section(BaseModel):
    heading: str
    content : str
    content2 : Optional[str] = None
    content3 : Optional[str] = None
    content4 : Optional[str] = None
    content5 : Optional[str] = None
    content6 : Optional[str] = None
    
class information(BaseModel):
    phone_number: List[str]
    email : EmailStr

class BlogCreate(BaseModel):
    img: str
    title: str
    introduction: introduction
    section: List[section]
    conclusion: str
    contact_information : information
    
class BlogUpdate(BlogCreate):
    pass