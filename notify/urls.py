from django.urls import path
from . import views


urlpatterns = [

 path('recipients/<int:recipient_id>/', views.email_recipient, name='email_recipient'),
]
