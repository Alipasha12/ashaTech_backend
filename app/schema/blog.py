from pydantic import BaseModel,EmailStr
from typing import Optional,List

class introductions(BaseModel):
    overview: str
    heading: Optional[str] = None
 
class section(BaseModel):
    heading: str
    content : str
    content2 : Optional[str] = None
    keypoint : List[str] = None
    content3 : Optional[str] = None
    keypoin2 : List[str] = None
    content4 : Optional[str] = None
    keypoint3 : List[str] = None
    content5 : Optional[str] = None
    keypoint4 : List[str] = None
    content6 : Optional[str] = None
    
class titles(BaseModel):
    title: str
    title2: Optional[str] = None
    
class informations(BaseModel):
    phone_number: List[str]
    email : EmailStr

class conclusions(BaseModel):
    heading : str
    content : Optional[str] = None
    content1 : Optional[str] = None
    content2 : Optional[str] = None
    content3 : Optional[str] = None
    
class BlogCreate(BaseModel):
    img: str
    title: titles
    introduction: introductions
    section: List[section]
    conclusion: conclusions
    contact_information : informations
    
class BlogUpdate(BlogCreate):
    pass