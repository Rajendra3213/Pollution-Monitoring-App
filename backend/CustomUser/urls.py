from django.urls import path
from .views import EmailVerification,Home,LoginView,MapView,LogoutView,DonateListView,DonateCompleteView

app_name='CustomUser'
urlpatterns = [
    path('confirm-mail/',EmailVerification.as_view(),name="verify email"),
    path('',Home.as_view(),name="home_page"),
    path('login/',LoginView.as_view(),name="admin_login"),
    path('map/view/',MapView.as_view(),name="map_view"),
    path('user/logout/',LogoutView.as_view(),name="logout_user"),
    path('donation/all/',DonateListView.as_view(),name="donate_list"),
    path('make/donation/<int:id>/',DonateCompleteView.as_view(),name="make_donation")
]
