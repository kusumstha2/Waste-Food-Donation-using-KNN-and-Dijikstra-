from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from location.models import DonorLocation


@login_required
def save_location(request):
    
    if request.method == 'POST':
        print(f"User: {request.user}, Authenticated: {request.user.is_authenticated}")
        
        data = json.loads(request.body)
        user_type = data.get('user_type')
        print(user_type)
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        print(f"Received user_type: {user_type}")
        
        if user_type == 'donor' and hasattr(request.user, 'donor'):
                donor = request.user.donor
                print(f"Donor found: {donor}")  # This will print the donor instance
                DonorLocation.objects.update_or_create(
                    donor=donor,
                    defaults={'latitude': latitude, 'longitude': longitude},
                )
                return JsonResponse({'message': 'Donor location updated.'}, status=200)
        else:
                print(f"User {request.user} is not associated with a donor.")
                return JsonResponse({'error': 'Unauthorized access. No donor found.'}, status=400)

        return JsonResponse({'error': 'Invalid user type or unauthorized access.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@login_required
def update_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        is_online = data.get('is_online')

        if hasattr(request.user, 'donor'):
            donor = request.user.donor
            
            donor_location, created = DonorLocation.objects.update_or_create(
                donor=donor,
                defaults={'is_online': is_online}
            )

            return JsonResponse({'message': 'Donor status updated.'}, status=200)

        return JsonResponse({'error': 'User is not a donor.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import json
from location.models import RecipientLocation

@csrf_protect
@login_required
def save_recipient_location(request):
    """
    Save the recipient's location on login if not already saved.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if hasattr(request.user, 'recipient'):
            recipient = request.user.recipient

            # Check if a location already exists for this recipient
            recipient_location, created = RecipientLocation.objects.get_or_create(
                recipient=recipient,
                defaults={'latitude': latitude, 'longitude': longitude}
            )

            if not created:  # If the location already exists
                return JsonResponse({'message': 'Location already exists. Use the update feature.'}, status=400)

            return JsonResponse({'message': 'Location saved successfully.'}, status=200)

        return JsonResponse({'error': 'User is not a recipient.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


@login_required
def update_recipient_location(request):
    """
    Allow recipients to update their location.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if hasattr(request.user, 'recipient'):
            recipient = request.user.recipient

            # Update the existing location
            recipient_location = RecipientLocation.objects.filter(recipient=recipient).first()
            if recipient_location:
                recipient_location.latitude = latitude
                recipient_location.longitude = longitude
                recipient_location.is_updated = True
                recipient_location.save()

                return JsonResponse({'message': 'Location updated successfully.'}, status=200)
            else:
                return JsonResponse({'error': 'No initial location found. Save your location first.'}, status=400)

        return JsonResponse({'error': 'User is not a recipient.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

def chooselocation(request):
    return render(request, "choose-location.html")

