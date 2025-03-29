from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db import Base
from pydantic import BaseModel

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))


class UserCreate(BaseModel):
    name: str
    password: str

class Criminal(Base):
    __tablename__ = "criminals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    crime_type = Column(String(100), nullable=False)
    
    # Relationship with cases
    cases = relationship("Case", back_populates="criminal")

class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    case_title = Column(String(200), nullable=False)
    description = Column(String(500), nullable=False)
    date_reported = Column(DateTime, nullable=False)
    criminal_id = Column(Integer, ForeignKey("criminals.id"))

    # Relationship with Criminal
    criminal = relationship("Criminal", back_populates="cases")
