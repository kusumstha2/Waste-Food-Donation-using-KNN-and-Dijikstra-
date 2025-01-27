from django.urls import path
from location.views import *
app_name='location'
from . import views
from .views import save_location


urlpatterns = [
    path('savelocation/', save_location, name='save-location'),
    path('update-status/', update_status, name='update_status'),

    path('update-recipient-location/', views.update_recipient_location, name='update_recipient_location'),
    path('choose-location/',chooselocation,name="choose-location"),
    path('saveuserlocation/',save_recipient_location,name="saveuserlocation"),
    
]




