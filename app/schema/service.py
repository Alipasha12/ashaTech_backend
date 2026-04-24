from pydantic import BaseModel
from typing import List, Optional

class introductions(BaseModel):
    heading: str
    content: str
    
class chooses(BaseModel):
    heading: str
    content: str

class Sections(BaseModel):
    heading: str
    content: str
    
class technologies(BaseModel):
    img: str
    heading: str
    content: str
    
class ServiceResponse(BaseModel):
    title: str
    img: str
    introduction: introductions
    choose_us: chooses
    section: List[Sections]
    technologies: List[technologies]