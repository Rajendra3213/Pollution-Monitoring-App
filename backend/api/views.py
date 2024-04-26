from datetime import datetime
from ninja import Router,NinjaAPI,Form,File
from ninja.files import UploadedFile
from CustomUser.models import User,EmailConfirm,UserPoint,TreePlantation
from django.contrib.auth import authenticate
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.html import strip_tags
import os
from .schema import RefreshIn,LoginIn,RegisterIn,UserComplainIn,UserComplainListOut,UserLocationIn,EventOut,TreeOut
from .auth import CustomHttpBearer,get_tokens_for_user
from event.models import Event
from complain.models import UserComplain,ValidationAuthority
from typing import List
from django.db.models import Q
from django.http import JsonResponse
import pickle5 as pickle
import pandas as pd
from django.conf import settings

router = Router()

@router.post('register/')
def registerUser(request,data:RegisterIn):
    if User.objects.filter(email=data.email).exists():
        return NinjaAPI().create_response(request,{"detail":"Email already exists"},status=404)
    user = User.objects.create_user(email=data.email,
        password=data.password,
        first_name=data.first_name,
        last_name=data.last_name,
        phone_number=data.phone_number,
        address=data.address,
        age=data.age)
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
    return {"detail": "User registered successfully,Check your email for verification"}

            
@router.get('check/',auth=CustomHttpBearer())
def check(request):
    if request.auth is None:
        return 401
    return {"detail":"Token Valid"}


@router.post('login/')
def loginUser(request,logindata:LoginIn):
    register_user=get_object_or_404(User,email=logindata.email)
    if register_user is None:
        return NinjaAPI().create_response(request,{"detail":"User not found"},status=400)
    user=authenticate(email=logindata.email,password=logindata.password)
    if user is None:
        return NinjaAPI().create_response(request,{"detail":"Email or password incorrect"},status=400)
    else:
        if user.is_active==False:
            return NinjaAPI().create_response(request,{"detail":"User is inactive Check your email!"},status=401)
        else:
            if user is not None:
                return get_tokens_for_user(user)
        

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
        lon_index=str(data.longitude).index('.')
        lat_index=str(data.latitude).index('.')
        rounded_longitude = float(str(data.longitude)[:lon_index+3])
        rounded_latitude = float(str(data.latitude)[:lat_index+3])
        validation=ValidationAuthority.objects.filter(
        Q(longitude__startswith=rounded_longitude)|
        Q(latitude__startswith=rounded_latitude)).first()
        user_complain=UserComplain.objects.create(
            longitude=data.longitude,
            latitude=data.latitude,
            complain_user=user,
            image=file,
            description=data.description,
            severity_level=data.severity_level,
            validated_by=validation
        )
        user_complain.save()
        user_point, created = UserPoint.objects.get_or_create(user=user, defaults={'point': 0})
        user_point.point += 10
        user_point.save()
        return  NinjaAPI().create_response(request,{"detail":"Complain Sucessfully Added"},status=201)

@router.post('complain/list',auth=CustomHttpBearer(),response=List[UserComplainListOut])
def get_complain_list(request,data:UserLocationIn):
    if request.auth is None:
        return 401
    else:
        lon_index=str(data.longitude).index('.')
        lat_index=str(data.latitude).index('.')
        rounded_longitude = float(str(data.longitude)[:lon_index+3])
        rounded_latitude = float(str(data.latitude)[:lat_index+3])
        usercomplains = UserComplain.objects.filter(
        Q(longitude__startswith=rounded_longitude)&
        Q(latitude__startswith=rounded_latitude)&
        Q(solved=False)
        )
        response_data = list(usercomplains.values("id", "longitude", "latitude"))
        return JsonResponse(response_data, safe=False)

@router.get('complain/select/{id}',auth=CustomHttpBearer())
def get_single_complain_data(request,id:int):
    if request.auth is None:
        return 401
    else:
        complain_data=get_object_or_404(UserComplain,id=id)
        return NinjaAPI().create_response(request,{
            "image":complain_data.image.url,
            "description":complain_data.description,
            "date":complain_data.date_of_complain,
            "severity_level":complain_data.severity_level,
            "validated_by":complain_data.validated_by.name,
            "contact":complain_data.validated_by.contact
        },status=201)

@router.get('event/all',auth=CustomHttpBearer(),response=List[EventOut])
def get_all_events(request):
    if request.auth is None:
        return 401
    else:
        current_time = datetime.now()
        event_list = Event.objects.filter(start_date__gt=current_time)
        return list(event_list.values("id","title","start_date","end_date","image","location","description"))
    
@router.get('event/detail/{id}',auth=CustomHttpBearer())
def get_single_event(request,id:int):
    if request.auth is None:
        return 401
    else:
        event=get_object_or_404(Event,id=id)
        return NinjaAPI().create_response(request,{
            "id":event.id,
            "title":event.title,
            "description":event.description,
            "image":event.image.url,
            "start_date":event.start_date,
            "end_date":event.end_date,
            "location":event.location
        },status=200)
    
@router.post('event/signup/{id}',auth=CustomHttpBearer())
def signup_event(request,id:int):
    if request.auth is None:
        return 401
    else:
        user_id=request.auth[1]['user_id']
        user=get_object_or_404(User,id=user_id)
        event=get_object_or_404(Event,id=id)
        event.signed_users.add(user)
        event.save()
        user_point, created = UserPoint.objects.get_or_create(user=user, defaults={'point': 0})
        user_point.point += 10
        user_point.save()
        plain_message=f"You have sucessfully signed up for {event.title}"
        message=EmailMultiAlternatives(
        subject="WasteWatch Nepal Event Signup!!",
        body=plain_message,
        from_email=None,
        to=[user.email]
    )
        message.send()
        return NinjaAPI().create_response(request,{'detail':'Sucessfully Registered for the event'},status=202)
    
@router.get('data/',auth=CustomHttpBearer())
def get_user_data(request):
    if request.auth is None:
        return 401
    else:
        user_id=request.auth[1]['user_id']
        user=get_object_or_404(User,id=user_id)
        try:
            userpoint = UserPoint.objects.get(user=user)
            point = userpoint.point
        except UserPoint.DoesNotExist:
            point = 0
        return NinjaAPI().create_response(request,{
            'email':user.email,
            "first_name":user.first_name,
            "last_name":user.last_name,
            "number":user.phone_number,
            "address":user.address,
            "age":user.age,
            "point":point
            },status=202)
    
@router.get('plantation/',auth=CustomHttpBearer(),response=list[TreeOut])
def get_all_plantation(request):
    if request.auth is None:
        return 401
    else:
        user_id=request.auth[1]['user_id']
        user=get_object_or_404(User,id=user_id)
        try:
            trees=TreePlantation.objects.filter(user=user,planted=True)
            return list(trees.values("latitude","longitude","planted"))
        except TreePlantation.DoesNotExist:
            return NinjaAPI().create_response(request,{},status=200)

@router.post('donate/plant/', auth=CustomHttpBearer())
def donate_plant(request):
    if request.auth is None:
        return 401
    else:
        user_id = request.auth[1]['user_id']
        user = get_object_or_404(User, id=user_id)
        try:
            userpoint = UserPoint.objects.get(user=user)
            point = userpoint.point
        except UserPoint.DoesNotExist:
            userpoint = UserPoint.objects.create(user=user, point=0)
            point = 0

        if point > 1000:
            try:
                tree = TreePlantation.objects.create(user=user)
                plain_message = "Thank you for your donation. We will update you via email when the plantation is completed."
                message = EmailMultiAlternatives(
                    subject="WasteWatch Nepal Tree Donation!",
                    body=plain_message,
                    from_email=None,
                    to=[user.email]
                )
                message.send()
                userpoint.point = userpoint.point - 1000
                userpoint.save()
                return NinjaAPI().create_response(request, {"detail": "Donation Successful! Plantation Pending"}, status=200)
            except:
                return NinjaAPI().create_response(request, {"detail": "Error"}, status=400)
        else:
            return NinjaAPI().create_response(request, {"detail": "Not enough points"}, status=400)

def make_severity(latitude,longitude):
    model_path =settings.BASE_DIR/"static/severity_model.pkl"
    print(model_path)
    with open(model_path, "rb") as f:
        model = pickle.load(f)
        data_to_predict = pd.DataFrame({'Longitude': [longitude], 'Latitude': [latitude]})

        severity_prediction = model.predict(data_to_predict)
        return severity_prediction

@router.post('predict/', auth=CustomHttpBearer())
def get_predicted_severity(request,data:UserLocationIn):
    if request.auth is None:
        return 401
    else:
        severity=make_severity(data.longitude,data.longitude)
        return {"severity":severity[0]}
    
@router.get('leaderboard/',auth=CustomHttpBearer())
def get_leaderboard_list(request):
    if request.auth is None:
        return 401
    else:
        leaderboard_list=list()
        user_points = UserPoint.objects.order_by('-point')
        if len(user_points)==0:
            return {}
        else:
            for up in user_points:
                dict={
                    "point":up.point,
                    "name":up.user.get_full_name(),
                    "tree_planted":TreePlantation.objects.filter(user=up.user).count()
                }
                leaderboard_list.append(dict)
        return leaderboard_list