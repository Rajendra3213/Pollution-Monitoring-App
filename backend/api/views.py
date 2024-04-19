from ninja import Schema,Router
from CustomUser.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from ninja.security import HttpBearer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

router = Router()

class RegisterIn(Schema):
    email:str
    password:str
    first_name:str|None=None
    last_name:str|None=None
    phone_number:str|None=None
    address:str|None=None


class LoginIn(Schema):
    email:str
    password:str

@router.post('register/')
def registerUser(request,data:RegisterIn):
    if User.objects.filter(email=data.email).exists():
        return {"message": "Username already exists"}
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
    return {"msg":"validated"}

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
    return {"msg":"unsucessful login"}