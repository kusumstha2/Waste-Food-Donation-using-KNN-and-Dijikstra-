from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from location.models import RecipientLocation
from foodapp.models import *
from .utils import send_email_to_recipient  # Import the fixed function

def email_recipient(request, recipient_id):
    if request.method == 'POST':
        try:
            # Fetch the recipient location
            recipient_location = get_object_or_404(RecipientLocation, id=recipient_id)
            donor = request.user.donor  # Get the donor from the logged-in user
            donor_name = donor.user.username

            # Get the food_name from the POST request
            food_details = request.POST.get("food_name")
            if not food_details:
                messages.error(request, "Food details are required.")
                return redirect('email_recipient', recipient_id=recipient_id)

            # Ensure recipient exists
            recipient = recipient_location.recipient  # Assuming `recipient` is linked to `User`
            if not recipient or not recipient.user.email:
                messages.error(request, "Recipient email not found.")
                return redirect('email_recipient', recipient_id=recipient_id)

            # Email content
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

            # Send email using the recipient's ID
            send_email_to_recipient(subject, message, recipient.user.id)
            messages.success(request, "Email sent successfully to the recipient.")
        except Exception as e:
            messages.error(request, f"Failed to send email: {e}")

        return redirect('/')  # Adjust as needed for your home or success page
