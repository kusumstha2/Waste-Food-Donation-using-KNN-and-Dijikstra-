from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from location.models import RecipientLocation
from foodapp.models import *
from .utils import send_email_to_recipient  # Ensure this function is correctly implemented

def email_recipient(request, recipient_id):
    if request.method == 'POST':
        try:
            # Fetch the recipient location and ensure it exists
            recipient_location = get_object_or_404(RecipientLocation, id=recipient_id)
            recipient = recipient_location.recipient  # Assuming RecipientLocation links to a Recipient or User
            
            # Ensure the logged-in user is a donor
            if not hasattr(request.user, 'donor'):
                messages.error(request, "You must be a donor to send emails.")
                return render(request, 'email.html', {'recipient_id': recipient_id})
            
            donor = request.user.donor  # Get the donor from the logged-in user
            donor_name = donor.user.username

            # Get the food details from the POST request
            food_details = request.POST.get("food_name")
            if not food_details:
                messages.error(request, "Food details are required.")
                return render(request, 'email.html', {'recipient_id': recipient_id})

            # Ensure the recipient has an email
            if not recipient or not recipient.user.email:
                messages.error(request, "Recipient email not found.")
                return render(request, 'email.html', {'recipient_id': recipient_id})

            # Prepare the email content
            subject = "Food Donation Notification"
            message = f"""
            Hello,

            {donor_name} has donated food and would like to contact you.
            Here are the food details:
            {food_details}

            Please reply to coordinate the pickup or further arrangements.

            Regards,
            Food Donation System
            """

            # Send the email using the recipient's ID
            send_email_to_recipient(subject, message, recipient.user.email)  # Adjust the utility function as needed
            messages.success(request, "Email sent successfully to the recipient.")
            return render(request, 'email.html', {'recipient_id': recipient_id, 'success': True})

        except RecipientLocation.DoesNotExist:
            messages.error(request, "The specified recipient location does not exist.")
        except Exception as e:
            messages.error(request, f"An error occurred while sending the email: {e}")

        return render(request, 'email.html', {'recipient_id': recipient_id})

    # Handle non-POST requests (optional)
    return render(request, 'email.html', {'recipient_id': recipient_id})