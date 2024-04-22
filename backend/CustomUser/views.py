from django.shortcuts import render,HttpResponse,get_object_or_404
from django.views import View
from .models import User,EmailConfirm
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os
# Create your views here.

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