from django.shortcuts import render
from .models import *
# Create your views here.
from rest_framework  import viewsets,filters
from .serializer import *
from  rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.authentication import TokenAuthentication
from django.http import JsonResponse
from .utils import calculate_distance
from sklearn.neighbors import NearestNeighbors
import numpy as np
from django.http import JsonResponse
from geopy.distance import geodesic
from .models import Recipient
from django.http import JsonResponse
from .utils import notify_recipients
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views import View
from django.http import HttpResponseForbidden
class DonorViewSet(viewsets.ModelViewSet):
    queryset = FoodDonation.objects.all()
    serializer_class = RecipientSerializer
    filter_backends = (SearchFilter,DjangoFilterBackend)
    pagination_class=PageNumberPagination
    search_field = ('name',)
    
class RecipientViewSet(viewsets.ModelViewSet):
    queryset = FoodDonation.objects.all()
    serializer_class = RecipientSerializer
    filter_backends = (SearchFilter,DjangoFilterBackend)
    pagination_class=PageNumberPagination
    search_field = ('name',)
    # permission_classes = (isDonorReadOnly,)
    # authentication_classes = [TokenAuthentication]
    # permission_classes=(IsAuthenticated,)
    

    
from django.shortcuts import render

def index(request):
    return render(request,'index.html')

def aboutus(request):
    return render(request,'aboutus.html')
from django.shortcuts import render


from django.shortcuts import render, redirect




from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactUs

def contactus(request):
    if request.method == 'POST':
        # Get data from HTML form fields
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save data to the database
        if name and email and subject and message:  # Ensure all fields are filled
            contact_entry = ContactUs(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            contact_entry.save()

            messages.success(request, "Your message has been sent successfully!")
            return redirect('/contactus/')  # Replace 'contactus' with the name of your contact URL
        else:
            messages.error(request, "Please fill out all fields.")
    
    return render(request, 'contactus.html')


def serving(request):
    return render(request,'serving.html')



def food_donation(request):
    donations = FoodDonation.objects.all()  # Get all donations from the database
    return render(request, 'food donation.html', {'donations': donations})

from django.http import JsonResponse
from .models import FoodDonation

def donation_details(request, id):
    try:
        donation = FoodDonation.objects.get(pk=id)
        data = {
            'food_name': donation.food_name,
            'food_image_url': donation.food_image.url if donation.food_image else '',
            'donor_name': donation.donor_name,
            'food_type': donation.food_type,
            'description': donation.description,
            'expiry_date': donation.expiry_date,
            'location': donation.location,
        }
        return JsonResponse(data)
    except FoodDonation.DoesNotExist:
        return JsonResponse({'error': 'Donation not found'}, status=404)


def donate_food(request):
    user = request.user  # Get the logged-in user
    return render(request, 'profile.html', {
        'username': user.username,
        'email': user.email,
        'phone': user.phone,
        'address': user.address,
    })

    

def profile(request):
    return render(request,'profile.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

def donate_food(request):
    if request.method == 'POST':
        # Get data from the HTML form
        donor_name = request.POST.get('donorName')
        phone_number = request.POST.get('donorNumber')
        food_name = request.POST.get('foodName')
        food_type = request.POST.get('foodType')
        food_image = request.FILES.get('foodImage')  # For file upload
        description = request.POST.get('description')
        expiry_date = request.POST.get('expiryDate')
        location = request.POST.get('location')

        # Check if all required fields are filled
        if donor_name and phone_number and food_name and food_type and description and expiry_date and location:
            # Save the donation to the database
            donation = FoodDonation(
                donor_name=donor_name,
                phone_number=phone_number,
                food_name=food_name,
                food_type=food_type,
                food_image=food_image,
                description=description,
                expiry_date=expiry_date,
                location=location,
            )
            donation.save()
            
            messages.success(request, "Your donation has been submitted successfully!")
            return redirect('/food-donation/')  # Replace with your donation URL name
        
        else:
            messages.error(request, "Please fill out all fields.")
    donations = FoodDonation.objects.all()
    return render(request, 'donate.html', {'donations': donations})  # Render the donation template

def editdonation(request):
    return render(request,'edit donation page.html')


# views.py
from django.core.mail import send_mail
from django.conf import settings
from .utils import calculate_distance, knn_recipients
from django.http import JsonResponse

def notify_recipients(donation_id):
    try:
        donation = FoodDonation.objects.get(pk=donation_id)
        recipients = knn_recipients(donation)  # Assuming this is your KNN function

        # Iterate through the recipients and notify them
        for recipient in recipients:
            # Send email notification (Example)
            send_mail(
                subject=f"New Donation: {donation.foodName}",
                message=f"Hello {recipient.name},\n\nThere is a new donation available: {donation.foodName}. Please contact us if you're interested.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.contact_number],  # Assuming you have an email or contact field
            )
            # Or notify via SMS if you have an SMS service like Twilio
            # send_sms(recipient.contact_number, "New food donation available!")

        return JsonResponse({"message": "Notifications sent successfully"})

    except FoodDonation.DoesNotExist:
        return JsonResponse({"error": "Donation not found"}, status=404)

