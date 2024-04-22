from ninja import Router,NinjaAPI,Form,File
from ninja.files import UploadedFile
from CustomUser.models import User,EmailConfirm
from django.contrib.auth import authenticate
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.html import strip_tags
import os
from .schema import RefreshIn,LoginIn,RegisterIn,UserComplainIn,UserComplainListOut,UserLocationIn
from .auth import CustomHttpBearer,get_tokens_for_user,get_user_id_from_token
from complain.models import UserComplain
from typing import List

router = Router()

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
    email_confim=EmailConfirm(user=user)
    email_confim.save()
    backend_link=os.environ.get('BACKEND_URL')
    confirm_link=f'{backend_link}/confirm-mail/?token={email_confim.id}'
    context={
        "link":confirm_link
    }
    html_message=render_to_string("CustomUser/email_send.html",context=context)
    plain_message=strip_tags(html_message)
    message=EmailMultiAlternatives(
        subject="WasteWatch Email Confirmation!!",
        body=plain_message,
        from_email=None,
        to=[user.email]
    )
    message.attach_alternative(html_message,'text/html')
    message.send()
    return {"message": "User registered successfully"}

            
@router.get('check/',auth=CustomHttpBearer())
def check(request):
    if request.auth is None:
        return 401
    return {"msg":"Token Valid"}


@router.post('login/')
def loginUser(request,logindata:LoginIn):
    user=authenticate(email=logindata.email,password=logindata.password)
    if user.is_active==False:
        return NinjaAPI().create_response(request,{"detail":"User is inactive"},status=401)
    else:
        if user is not None:
            return get_tokens_for_user(user)
    return NinjaAPI().create_response(request,{"detail":"User not found"},status=400)

@router.post('token/refresh/')
def tokenRefresh(request,data:RefreshIn):
    checkToken=RefreshToken(data.refresh,verify=False)
    is_expired=checkToken.get('exp')<timezone.now().timestamp()
    if not is_expired:
        return NinjaAPI().create_response(request,{"access":str(checkToken.access_token)},status=201)
    return NinjaAPI().create_response(request,{"detail":"token is expired"},status=401)

@router.post('complain/add',auth=CustomHttpBearer())
def add_complain(request,data:UserComplainIn=Form(...),file:UploadedFile=File(...)):
    if request.auth is None:
        return 401
    else:
        user_id=request.auth[1]['user_id']
        user=get_object_or_404(User,id=user_id)
        user_complain=UserComplain.objects.create(
            longitude=data.longitude,
            latitude=data.latitude,
            complain_user=user,
            image=file,
            description=data.description
        )
        user_complain.save()
        return  NinjaAPI().create_response(request,{"detail":"upload sucessful"},status=201)

@router.post('complain/list',auth=CustomHttpBearer(),response=List[UserComplainListOut])
def get_complain_list(request,data:UserLocationIn):
    lon_index=str(data.longitude).index('.')
    lat_index=str(data.latitude).index('.')
    rounded_longitude = float(str(data.longitude)[:lon_index+4])
    rounded_latitude = float(str(data.latitude)[:lat_index+4])
    print(rounded_longitude,rounded_latitude)
    usercomplains = UserComplain.objects.filter(
    longitude__startswith=rounded_longitude,
    latitude__startswith=rounded_latitude
    )
    print(usercomplains)
    return list(usercomplains.values("id", "longitude", "latitude"))
