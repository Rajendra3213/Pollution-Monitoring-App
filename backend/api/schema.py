from pydantic import BaseModel,EmailStr,ValidationError,field_validator,Field
import re
class RegisterIn(BaseModel):
    email:EmailStr
    password:str
    first_name:str|None=None
    last_name:str|None=None
    phone_number:str|None=None
    address:str|None=None

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

    @field_validator('password')
    def validate_password(cls,value):
        pattern=r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
        if not re.match(pattern,value):
            raise ValueError("Enter a valid password")
        return value

class RefreshIn(BaseModel):
    refresh:str


class UserComplainIn(BaseModel):
    longitude: float
    latitude: float
    description: str

class UserComplainListOut(BaseModel):
    id: int
    longitude: float
    latitude: float

    class Config:
        orm_mode = True

class UserLocationIn(BaseModel):
    longitude: float
    latitude: float