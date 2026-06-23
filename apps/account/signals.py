# ============================================================
# signals.py
# Yeh file Django Signals handle karti hai.
# Signal matlab — jab koi event ho (jaise order ship ho),
# toh automatically kuch action trigger ho jaye.
# Hume manually har jagah code likhne ki zaroorat nahi.
# ============================================================

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OTP, User
from .views import generate_otp, send_otp_email




# ============================================================
#  Naya User register hone pe automatically OTP bhejo
# Yeh signal tab chalega jab naya User object database mein save ho.
# "created=True" matlab bilkul naya user hai, update nahi.
# ============================================================

@receiver(post_save, sender=User)
def send_otp_on_register(sender, instance, created, **kwargs):

    # Sirf naye user ke liye chale, aur jo abhi active nahi hai
    if created and not instance.is_active:

        # OTP generate karke database mein save karo
        otp_code = generate_otp()
        OTP.objects.create(
            email=instance.email,
            code=otp_code
        )

        # Email bhejo
        send_otp_email(instance.email, otp_code)