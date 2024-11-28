import time
from django_rq import job




@job
def send_verification_email(recipient_list):

    subject = "Welcome"
    message = "click on the link to verify your account {}"
    try:
        # Create the email message
        email = EmailMessage(
            subject=subject,
            body=message,
            to=recipient_list,
            from_email=from_email,
        )

        # Send the email
        email.send(fail_silently=False)
        print("sent")
        return True

    except Exception as e:
        # Log or handle errors
        print(f"Failed to send email: {str(e)}")
        return False
