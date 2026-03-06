from pydantic import BaseModel
from typing import List

class section(BaseModel):
    title:str
    desc:str
 
class choose_us(BaseModel):
    title:str
    description:str   


class section2(BaseModel):
    title:str
    description:str
  
class technologies(BaseModel):
    img: str
    title: str
    desc: str  

class SeviceCreate(BaseModel):
    category: str
    img:str 
    section:section
    choose_us: choose_us
    section2:List[section2]
    technologies: List[technologies]
    
class serviceUpdate(SeviceCreate):
    pass