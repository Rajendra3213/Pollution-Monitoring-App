from django.urls import path
from .views import EmailVerification
urlpatterns = [
    path('confirm-mail/',EmailVerification.as_view(),name="verify email"),
]
