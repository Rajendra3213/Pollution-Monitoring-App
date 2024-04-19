from ninja import Router,NinjaAPI
from CustomUser.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from ninja.security import HttpBearer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from pydantic import BaseModel,EmailStr,ValidationError,field_validator,Field
import re
from django.utils import timezone

router = Router()

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

@router.post('register/')
def registerUser(request,data:RegisterIn):
    if User.objects.filter(email=data.email).exists():
        return {"message": "Email already exists"}
    user = User.objects.create_user(email=data.email,
        password=data.password,
        first_name=data.first_name,
        last_name=data.last_name,
        phone_number=data.phone_number,
        address=data.address)
    return {"message": "User registered successfully"}

class CustomHttpBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            authentication = JWTAuthentication()
            validated_token = authentication.get_validated_token(token)
            user = authentication.get_user(validated_token)
            return user, validated_token
        except InvalidToken:
            return None
            
@router.get('check/',auth=CustomHttpBearer())
def check(request):
    if request.auth is None:
        return 401
    return {"msg":"Token Valid"}

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "msg":"sucessful login",
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
@router.post('login/')
def loginUser(request,logindata:LoginIn):
    user=authenticate(email=logindata.email,password=logindata.password)
    if user is not None:
        return get_tokens_for_user(user)
    return {"msg":"User does not exist"}

@router.post('token/refresh/')
def tokenRefresh(request,data:RefreshIn):
    checkToken=RefreshToken(data.refresh,verify=False)
    is_expired=checkToken.get('exp')<timezone.now().timestamp()
    if not is_expired:
        return NinjaAPI().create_response(request,{"access":str(checkToken.access_token)},status=201)
    return NinjaAPI().create_response(request,{"detail":"token is expired"},status=401)