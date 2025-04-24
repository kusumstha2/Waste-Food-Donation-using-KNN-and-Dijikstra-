from django.urls import path
from . import views

urlpatterns = [
    # URL pattern for sending email to the recipient
    path('recipients/<int:recipient_id>/', views.email_recipient, name='email_recipient'),
]  