from pydantic import BaseModel
from typing import List, Optional

class Section(BaseModel):
    heading: str
    content: str
    content2: Optional[str] = None
    content3: Optional[str] = None
    content4: Optional[str] = None
    content5: Optional[str] = None
    content6: Optional[str] = None

    class Config:
        orm_mode = True


class ChooseUs(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class Section2(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class Technology(BaseModel):
    img: str
    title: str
    desc: str

    class Config:
        orm_mode = True


class ServiceResponse(BaseModel):
    title: str
    img: str
    introduction: dict
    contact_information: dict
    conclusion: str
    section: list[Section]

    class Config:
        orm_mode = True