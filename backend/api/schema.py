from pydantic import BaseModel,EmailStr,ValidationError,field_validator,Field,AnyUrl
from datetime import datetime
from typing import List,Optional
import re
from enum import Enum

class RegisterIn(BaseModel):
    email:EmailStr
    password:str
    first_name:str|None=None
    last_name:str|None=None
    phone_number:str|None=None
    address:str|None=None
    age:int

    @field_validator('password')
    def validate_password(cls,value):
        pattern=r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
        if not re.match(pattern,value):
            raise ValueError("Enter a valid password")
        return value
    @field_validator('phone_number')
    def validate_number(cls,value):
        pattern=r'\+?\d{10,}'
        if not re.match(pattern,value):
            raise ValueError("Enter a valid number")
        return value

class LoginIn(BaseModel):
    email:EmailStr
    password:str

class RefreshIn(BaseModel):
    refresh:str

class SeverityLevelEnum(str, Enum):
    VERY_MINIMUM = 'very_minimum'
    LOW = 'low'
    HIGH = 'high'
    VERY_HIGH = 'very_high'

class UserComplainIn(BaseModel):
    longitude: float
    latitude: float
    description: str
    severity_level: SeverityLevelEnum

class UserComplainListOut(BaseModel):
    id: int
    longitude: float
    latitude: float

class UserLocationIn(BaseModel):
    longitude: float
    latitude: float

class EventOut(BaseModel):
    id: int
    title: str
    image:str
    start_date: datetime
    end_date:datetime
    location:str
    description:str

class TreeOut(BaseModel):
    longitude: float|None
    latitude: float|None
    planted:bool