from django.urls import path
from .views import *

app_name='CustomUser'
urlpatterns = [
    path('confirm-mail/',EmailVerification.as_view(),name="verify email"),
    path('dashboard/',Dashboard.as_view(),name="dashboard"),
    path('',Home.as_view(),name="home_page"),
    path('login/',LoginView.as_view(),name="admin_login"),
    path('map/view/',MapView.as_view(),name="map_view"),
    path('user/logout/',LogoutView.as_view(),name="logout_user"),
    path('donation/all/',DonateListView.as_view(),name="donate_list"),
    path('make/donation/<int:id>/',DonateCompleteView.as_view(),name="make_donation"),
    path('event/list/',EventView.as_view(),name="event_list"),
    path('tree/view/',TreeMapView.as_view(),name="tree_view"),
    path('report/',ReportGeneration.as_view(),name="report"),
    path('downloadcsv/',DownloadCSV.as_view(),name="download")
]
