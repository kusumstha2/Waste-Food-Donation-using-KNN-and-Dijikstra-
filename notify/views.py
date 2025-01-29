from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from location.models import RecipientLocation
from foodapp.models import *
from .utils import *


def email_recipient(request, recipient_id):
    if request.method == 'GET':
        recipient_location = get_object_or_404(RecipientLocation, id=recipient_id)
        return render(request, 'email.html', {'recipient': recipient_location})

    if request.method == 'POST':
        try:
            # Get donor and food details
            donor = request.user.donor
            donor_name = donor.user.username
            food_details = request.POST.get("food_name")

            if not food_details:
                messages.error(request, "Food details are required.")
                return redirect('email_recipient', recipient_id=recipient_id)

            # Get recipient email
            recipient_location = get_object_or_404(RecipientLocation, id=recipient_id)
            recipient_email = recipient_location.recipient.user.email

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

            # Send email
            send_email_to_recipient(subject, message, recipient_email)
            messages.success(request, "Email sent successfully to the recipient.")
        except Exception as e:
            messages.error(request, f"Failed to send email: {e}")

        return redirect('/home/')  # Replace with your actual redirect URL
