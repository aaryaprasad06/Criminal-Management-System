from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CaseBase(BaseModel):
    case_title: str
    description: str
    date_reported: datetime

class CaseCreate(CaseBase):
    criminal_id: int

class CaseResponse(CaseBase):
    id: int
    criminal_id: int

    class Config:
        orm_mode = True

class CriminalBase(BaseModel):
    name: str
    age: int
    crime_type: str

class CriminalCreate(CriminalBase):
    pass

class CriminalResponse(CriminalBase):
    id: int
    cases: List[CaseResponse] = []

    class Config:
        orm_mode = True



class UserCreate(BaseModel):
    name: str
    password: str

class UserLogin(BaseModel):
    name: str
    password: str

class CaseCreate(BaseModel):
    title: str
    description: str
    crime_type: str
    suspect_name: str
    location: str

class CaseResponse(BaseModel):
    id: int
    title: str
    description: str
    crime_type: str
    suspect_name: str
    location: str