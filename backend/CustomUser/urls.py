from django.urls import path
from .views import EmailVerification,Home
urlpatterns = [
    path('confirm-mail/',EmailVerification.as_view(),name="verify email"),
    path('',Home.as_view(),name="home_page")
]
