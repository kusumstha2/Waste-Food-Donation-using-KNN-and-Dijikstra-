# from django.urls import path, include
# from django.contrib.auth.models import User
# from .views import LoginAPIView,LogoutAPIView,RegistrationAPIView


# urlpatterns = [
#    path('register/',RegistrationAPIView.as_view(),name='user-registration'),
#    path('login/',LoginAPIView.as_view(),name='user-login'),
#    path('logout/',LogoutAPIView.as_view(),name= 'user-logout'),
   
# ]

from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()

# router.register(r'user',UserViewset,basename='user')
# router.register(r'otp-verification',OTPVerificationViewset,basename='otp-verification')

app_name = 'authentication' 
from .  import views
urlpatterns = [
    path('donor/signup/', DonorSignupView.as_view(), name='donor-signup'),
    path('donor/login/', DonorLoginView.as_view(), name='donor-login'),
    path('recipient/signup/', RecipientSignupView.as_view(), name='recipient-signup'),
    path('recipient/login/', RecipientLoginView.as_view(), name='recipient-login'),
    path('dashboard/',Dashboard.as_view(), name='dashboard'),
    path('logout/',logout.as_view(), name='logout'),
    path("profile/", profile_view, name="profile"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
