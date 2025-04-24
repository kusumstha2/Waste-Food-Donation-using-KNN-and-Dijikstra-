from django.urls import path, include
from rest_framework import routers
from .views import *
from .  import views
app_name= "foodapp"

router = routers.SimpleRouter()
router.register(r'recipients',RecipientViewSet,basename='recipient')
router.register(r'donors',DonorViewSet,basename='donor')

urlpatterns = [
    # path('notify-recipients/<int:donation_id>/', notify_recipients, name='notify_recipients'),
    path('',index, name='index'),
    path('aboutus/',views.aboutus, name='aboutus'),
    path('contactus/',views.contactus, name='contactus'),
    path('serving/',views.serving, name='serving'),
    
    path('donate/', views.donate_food, name='donate_food'),
    path('food-donation/',views.food_donation, name='food-donation'),
    path('donation_details/<int:id>/', views.donation_details, name='donation_details'),
    path('editdonation/', views.editdonation, name='editdonation'),
]

