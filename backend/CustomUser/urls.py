from django.urls import path
from .views import EmailVerification,Home,LoginView,MapView

app_name='CustomUser'
urlpatterns = [
    path('confirm-mail/',EmailVerification.as_view(),name="verify email"),
    path('',Home.as_view(),name="home_page"),
    path('login/',LoginView.as_view(),name="admin_login"),
    path('map/view/',MapView.as_view(),name="map_view")
]
