from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from django.views.generic import TemplateView
from .models import User,EmailConfirm,UserPoint,TreePlantation
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os
import folium
from .forms import LoginForm,DonationForm
from django.contrib.auth import authenticate,login,logout
from complain.models import UserComplain
from django.template.loader import render_to_string
import branca
from django.contrib.auth.mixins import LoginRequiredMixin

class Home(View):
    def get(self,request):
        return render(request,"CustomUser/landing_page.html")
    
class EmailVerification(View):

    def get(self,request):
        token=request.GET.get('token')
        email=get_object_or_404(EmailConfirm,id=token)
        if email.time_valid>timezone.now():
            user=get_object_or_404(User,id=email.user.id)
            user.is_active=True
            user.save()
            verification=True
        else:
            verification=False
        context={
            "verified":verification
        }
        return render(request,"CustomUser/email_verification.html",context=context)
    def post(self,request):
        try:
            token=request.GET.get('token')
            email=get_object_or_404(EmailConfirm,id=token)
            user=get_object_or_404(User,id=email.user.id)
            email_confim=EmailConfirm(user=user)
            email.delete()
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
            sucessful=True
        except:
            sucessful=False
        return render(request,"CustomUser/email_resend.html",context={"sucess":sucessful})
    
class LoginView(View):
    def get(self,request):
        return render(request,'CustomUser/login.html',{'form':LoginForm()})
    def post(self,request):
        loginVal=LoginForm(request.POST)
        if loginVal.is_valid():
            email=loginVal.cleaned_data['email']
            password=loginVal.cleaned_data['password']
            getUser=authenticate(email=email,password=password)
            if getUser is not None:
                if getUser.is_superuser:
                    login(request,getUser)
                    return redirect('CustomUser:home_page')
                else:
                    loginVal.add_error(None,'Only superuser can login')
                    return render(request,'CustomUser/login.html',{'form':loginVal})
        loginVal.add_error(None,'Error Email or password')
        return render(request,'CustomUser/login.html',{'form':loginVal})
    
def make_markers_and_add_to_map(map, complain):
    backend_url=os.environ.get("BACKEND_URL")
    html_code = render_to_string('CustomUser/popover.html',context={"c":complain,"b_url":backend_url})
    iframe = branca.element.IFrame(html=html_code,width="300px",height="400px")
    popup = folium.Popup(iframe,max_width="300px")
    folium.Marker(
            location = [complain.latitude, complain.longitude],
            popup = popup,
            tooltip = complain,
            icon = folium.Icon(icon='fa-trash', prefix='fa')
        ).add_to(map)
    
class MapView(LoginRequiredMixin,TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('CustomUser:admin_login')
        return super().dispatch(request, *args, **kwargs)
    
    template_name = 'CustomUser/map.html'    

    def get_context_data(self, **kwargs):
        figure = folium.Figure()
        map = folium.Map(
            location = [27.680677, 85.326492],
            zoom_start = 14,
            tiles = 'OpenStreetMap')

        map.add_to(figure)
        
        for complain in UserComplain.objects.all():
            make_markers_and_add_to_map(map, complain)
        
        figure.render()
        return {"map": figure}
    
class LogoutView(LoginRequiredMixin,View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('CustomUser:login')
        return super().dispatch(request, *args, **kwargs)
    def get(self,request):
        logout(request)
        return redirect('CustomUser:home_page')
    
class DonateListView(LoginRequiredMixin,View):
    def get(self,request):
        donations=TreePlantation.objects.filter(planted=False)
        return render(request,"CustomUser/donation_pending_list.html",context={'donations':donations})
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('CustomUser:login')
        return super().dispatch(request, *args, **kwargs)
    
class DonateCompleteView(LoginRequiredMixin, View):
    def get(self, request, id):
        return render(request, "CustomUser/make_donation.html", context={'form': DonationForm, 'id': id})

    def post(self, request, id):
        donation = get_object_or_404(TreePlantation, pk=id)
        print(donation.user.email)
        donate_form = DonationForm(request.POST, instance=donation)
        if donate_form.is_valid():
            donate_form.save()
            plain_message = "Your donation Tree has been planted."
            message = EmailMultiAlternatives(
            subject="WasteWatch Nepal Tree Sucessful Donation!",
            body=plain_message,
            from_email=None,
            to=[donation.user.email]
            )
            message.send()
            return redirect("CustomUser:donate_list")
        return render(request, "CustomUser/make_donation.html", context={'form': donate_form})
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('CustomUser:login')
        return super().dispatch(request, *args, **kwargs)