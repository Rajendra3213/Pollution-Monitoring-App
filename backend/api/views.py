from ninja import NinjaAPI,Schema
from CustomUser.models import User
from django.contrib.auth import authenticate

api = NinjaAPI()

class RegisterIn(Schema):
    email:str
    password:str
    first_name:str|None=None
    last_name:str|None=None
    phone_number:str|None=None
    address:str|None=None
class RegisterOut(Schema):
    email:str
    first_name:str|None=None
    last_name:str|None=None
    phone_number:str|None=None
    address:str|None=None

class LoginIn(Schema):
    email:str
    password:str

@api.post('/register/')
def add(request,data:RegisterIn):
    if User.objects.filter(email=data.email).exists():
        return {"message": "Username already exists"}
    user = User.objects.create_user(email=data.email,
        password=data.password,
        first_name=data.first_name,
        last_name=data.last_name,
        phone_number=data.phone_number,
        address=data.address)
    return {"message": "User registered successfully"}

@api.post('/login/')
def add(request,data:LoginIn):
    user=authenticate(email=data.email,password=data.password)
    print(user)
    if user is not None:
        return {"msg":"sucessful login"}
    return {"msg":"unsucessful login"}