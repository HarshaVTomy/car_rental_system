from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking

@receiver(post_save, sender=Booking)
def notify_user_on_status_change(sender, instance, **kwargs):
    if instance.status == 'Confirmed':
        subject = "Booking Confirmed"
        message = f"Dear {instance.user.username}, your booking (ID: {instance.id}) has been confirmed. You can now proceed to payment."
        instance.user.email_user(subject, message)
